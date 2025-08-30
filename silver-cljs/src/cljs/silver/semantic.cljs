(ns silver.semantic
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(def concept-boost-weights
  {"technology" 1.4
   "system" 1.3
   "complexity" 1.5
   "simple" 1.4
   "thinking" 1.3
   "understanding" 1.4
   "question" 1.3
   "human" 1.2
   "interface" 1.3
   "design" 1.2})

(defn extract-concepts [text]
  "Extract semantic concepts using NLP-like analysis"
  (let [words (->> (str/split (str/lower-case text) #"[^a-zA-Z0-9\-]+")
                   (filter #(> (count %) 3))
                   frequencies)
        high-freq-words (filter #(>= (val %) 2) words)
        bigrams (map str/join 
                     (partition 2 1 (take 50 (str/split (str/lower-case text) #"\s+"))))]
    (concat (map first high-freq-words) (take 10 bigrams))))

(defn calculate-complexity [text]
  "Multi-dimensional complexity scoring"
  (let [sentences (str/split text #"[.!?]+")
        words (str/split text #"\s+")
        unique-words (set words)
        avg-sentence-length (if (seq sentences)
                              (/ (count words) (count sentences))
                              0)
        lexical-diversity (if (seq words)
                            (/ (count unique-words) (count words))
                            0)
        abstract-concepts (count (filter #(contains? #{"system" "complexity" "understanding" 
                                                       "philosophy" "abstraction" "concept"} %) 
                                        (map str/lower-case words)))]
    (min 1.0 (+ (* 0.3 (min 1.0 (/ avg-sentence-length 25)))
                (* 0.4 lexical-diversity)  
                (* 0.3 (min 1.0 (/ abstract-concepts 10)))))))

(defn analyze-tone [text]
  "Enhanced emotional/intellectual tone analysis"
  (let [words (map str/lower-case (str/split text #"\s+"))
        positive-indicators ["good" "great" "beautiful" "wonderful" "amazing" "elegant" "powerful"]
        negative-indicators ["difficult" "problem" "wrong" "bad" "terrible" "broken" "failure"]
        contemplative-indicators ["think" "consider" "reflect" "ponder" "question" "perhaps" 
                                 "might" "could" "wonder" "explore"]
        technical-indicators ["system" "interface" "algorithm" "implementation" "architecture"]
        
        pos-count (count (filter (set positive-indicators) words))
        neg-count (count (filter (set negative-indicators) words))  
        cont-count (count (filter (set contemplative-indicators) words))
        tech-count (count (filter (set technical-indicators) words))]
    
    (cond
      (> tech-count (max pos-count neg-count cont-count)) :technical
      (> cont-count (max pos-count neg-count)) :contemplative
      (> pos-count neg-count) :positive
      (> neg-count pos-count) :critical
      :else :neutral)))

(defn analyze-structure [text]
  "Detect structural patterns in text"
  (cond
    (re-find #"##\s" text) :sectioned
    (re-find #"\d+\.\s" text) :enumerated
    (re-find #"[-*]\s" text) :listed
    (> (count (str/split text #"\n\n")) 4) :narrative
    :else :simple))

(defn enhance-document [doc]
  "Add semantic analysis to document from main server"
  (when-let [content (:content doc)]
    (let [concepts (extract-concepts content)
          complexity (calculate-complexity content)
          tone (analyze-tone content)
          structure (analyze-structure content)]
      (assoc doc
             :concepts concepts
             :complexity complexity
             :tone tone
             :structure structure
             :word-count (count (str/split content #"\s+"))
             :primary-cluster (classify-primary-cluster concepts tone)
             :semantic-vector (create-semantic-vector concepts)))))

(defn classify-primary-cluster [concepts tone]
  "Determine primary semantic cluster"
  (let [concept-set (set (map str/lower-case concepts))]
    (cond
      (some #(str/includes? % "technology") concepts) :technology
      (or (concept-set "complexity") (concept-set "simple")) :complexity
      (or (concept-set "thinking") (concept-set "philosophy")) :philosophy
      (concept-set "human") :humanity
      (= tone :technical) :technical
      :else :general)))

(defn create-semantic-vector [concepts]
  "Create weighted concept vector for similarity calculations"
  (reduce (fn [vector concept]
            (let [weight (get concept-boost-weights concept 1.0)
                  normalized-concept (str/lower-case concept)]
              (assoc vector normalized-concept weight)))
          {} concepts))

(defn cosine-similarity [vec1 vec2]
  "Calculate cosine similarity between semantic vectors"
  (let [all-concepts (set/union (set (keys vec1)) (set (keys vec2)))
        dot-product (reduce + (map #(* (get vec1 % 0) (get vec2 % 0)) all-concepts))
        norm1 (Math/sqrt (reduce + (map #(Math/pow (get vec1 % 0) 2) all-concepts)))
        norm2 (Math/sqrt (reduce + (map #(Math/pow (get vec2 % 0) 2) all-concepts)))]
    (if (or (zero? norm1) (zero? norm2))
      0
      (/ dot-product (* norm1 norm2)))))

(defn find-similar-documents [target-doc documents threshold]
  "Find semantically similar documents with live scoring"
  (when-let [target-vector (:semantic-vector target-doc)]
    (->> documents
         (remove #(= (:path %) (:path target-doc)))
         (map (fn [doc]
                (when-let [doc-vector (:semantic-vector doc)]
                  (let [similarity (cosine-similarity target-vector doc-vector)]
                    (assoc doc :similarity similarity)))))
         (filter #(and % (> (:similarity %) threshold)))
         (sort-by :similarity >)
         (take 5))))

(defn filter-documents [documents query selected-clusters complexity-range tone-filter]
  "Multi-tier live filtering system"
  (let [[min-complexity max-complexity] complexity-range]
    (->> documents
         ;; Text search filter
         (filter (fn [doc]
                   (if (empty? query)
                     true
                     (let [searchable-text (str (:name doc) " " 
                                               (str/join " " (:concepts doc)))]
                       (str/includes? (str/lower-case searchable-text)
                                     (str/lower-case query))))))
         ;; Cluster filter  
         (filter (fn [doc]
                   (if (empty? selected-clusters)
                     true
                     (contains? selected-clusters (:primary-cluster doc)))))
         ;; Complexity filter
         (filter (fn [doc]
                   (let [complexity (:complexity doc 0)]
                     (and (>= complexity min-complexity)
                          (<= complexity max-complexity)))))
         ;; Tone filter
         (filter (fn [doc]
                   (if (= tone-filter :all)
                     true
                     (= (:tone doc) tone-filter)))))))

(defn build-index [documents]
  "Build multi-tier search index for instant filtering"
  (let [concept-index (reduce (fn [idx doc]
                                (reduce (fn [cidx concept]
                                          (update cidx concept (fnil conj #{}) doc))
                                        idx (:concepts doc)))
                              {} documents)
        tone-index (group-by :tone documents)
        complexity-buckets (group-by #(int (* 10 (:complexity %))) documents)]
    {:concepts concept-index
     :tones tone-index  
     :complexity-buckets complexity-buckets
     :total-docs (count documents)}))