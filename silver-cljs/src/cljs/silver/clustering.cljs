(ns silver.clustering
  (:require [silver.semantic :as semantic]
            [clojure.set :as set]))

(defn semantic-clustering [documents]
  "Primary clustering by semantic similarity"
  (group-by :primary-cluster documents))

(defn temporal-clustering [documents]
  "Cluster by creation/modification patterns (simulated)"
  (let [now (.getTime (js/Date.))
        day-ms (* 24 60 60 1000)]
    (group-by (fn [doc] 
                (let [simulated-time (- now (* (hash (:path doc)) day-ms))]
                  (cond
                    (< simulated-time (* 7 day-ms)) :recent
                    (< simulated-time (* 30 day-ms)) :this-month  
                    (< simulated-time (* 90 day-ms)) :this-quarter
                    :else :older)))
              documents)))

(defn structural-clustering [documents]
  "Cluster by document structure patterns"
  (group-by :structure documents))

(defn complexity-clustering [documents]
  "Cluster by cognitive complexity levels"
  (group-by (fn [doc]
              (let [complexity (:complexity doc 0)]
                (cond
                  (< complexity 0.3) :simple
                  (< complexity 0.6) :moderate
                  :else :complex)))
            documents))

(defn hybrid-clustering [documents]
  "Multi-dimensional clustering combining several factors"
  (let [primary-clusters (semantic-clustering documents)]
    (reduce-kv (fn [result cluster-key cluster-docs]
                 (if (<= (count cluster-docs) 3)
                   ;; Small clusters stay as-is
                   (assoc result cluster-key cluster-docs)
                   ;; Large clusters get subdivided
                   (let [sub-clusters (complexity-clustering cluster-docs)]
                     (reduce-kv (fn [sub-result sub-key sub-docs]
                                  (let [combined-key (keyword (str (name cluster-key) 
                                                                  "-" (name sub-key)))]
                                    (assoc sub-result combined-key sub-docs)))
                                result sub-clusters))))
               {} primary-clusters)))

(defn stochastic-jitter [base-value variance-factor]
  "Add controlled randomness to clustering decisions"
  (let [jitter (* variance-factor (- (js/Math.random) 0.5))]
    (+ base-value jitter)))

(defn entropy-weighted-selection [options weights]
  "Select clustering method using entropy-based randomness"
  (let [total-weight (reduce + weights)
        normalized (map #(/ % total-weight) weights)
        rand-val (js/Math.random)]
    (loop [opts options
           norm normalized
           acc 0]
      (if (or (empty? opts) (< rand-val (+ acc (first norm))))
        (first opts)
        (recur (rest opts) (rest norm) (+ acc (first norm)))))))

(defn multi-tier-adaptive-clustering [documents similarity-threshold entropy-factor]
  "Sophisticated multi-tier clustering with diverse randomness sources"
  (let [doc-count (count documents)
        complexity-variance (if (> doc-count 1)
                             (let [complexities (map :complexity documents)
                                   mean (/ (reduce + complexities) doc-count)
                                   variance (/ (reduce + (map #(Math/pow (- % mean) 2) complexities)) 
                                              doc-count)]
                               variance)
                             0)
        tone-diversity (count (distinct (map :tone documents)))
        
        ;; Varied randomness sources
        time-seed (mod (.getTime (js/Date.)) 1000)
        content-seed (reduce + (map #(hash (:path %)) documents))
        stochastic-threshold (stochastic-jitter similarity-threshold 0.1)
        
        ;; Multi-dimensional decision matrix with controlled randomness
        clustering-weights [(+ 0.3 (* 0.2 (js/Math.sin (/ time-seed 100))))  ; temporal variance
                           (+ 0.2 (* complexity-variance 2))                    ; complexity-driven
                           (+ 0.15 (/ tone-diversity 10))                       ; tone diversity
                           (+ 0.25 (* 0.1 (js/Math.cos (/ content-seed 50))))  ; content-based variance
                           (* entropy-factor (js/Math.random))]                 ; pure entropy
        
        clustering-methods [semantic-clustering
                           complexity-clustering  
                           temporal-clustering
                           structural-clustering
                           hybrid-clustering]
        
        selected-method (entropy-weighted-selection clustering-methods clustering-weights)]
    
    ;; Apply selected clustering with stochastic threshold
    (let [base-clusters (selected-method documents)]
      ;; Post-process with cross-tier validation
      (reduce-kv (fn [result cluster-key docs]
                   (if (and (> (count docs) 3) 
                           (< (js/Math.random) stochastic-threshold))
                     ;; Randomly subdivide large clusters for exploration
                     (let [sub-method (rand-nth [complexity-clustering structural-clustering])
                           sub-clusters (sub-method docs)]
                       (merge result 
                              (reduce-kv (fn [sub-result sub-key sub-docs]
                                          (assoc sub-result 
                                                (keyword (str (name cluster-key) 
                                                            "-" (name sub-key)))
                                                sub-docs))
                                        {} sub-clusters)))
                     ;; Keep cluster as-is
                     (assoc result cluster-key docs)))
                 {} base-clusters))))

(defn dynamic-reclustering [documents similarity-threshold]
  "Enhanced real-time clustering with multi-tier randomness"
  (if (< (count documents) 10)
    ;; Small sets: simple semantic clustering with minor jitter
    (let [jittered-threshold (stochastic-jitter similarity-threshold 0.05)]
      (semantic-clustering documents))
    ;; Larger sets: full multi-tier adaptive clustering
    (multi-tier-adaptive-clustering documents similarity-threshold 0.3)))

(defn create-clusters [documents]
  "Main clustering entry point with multiple methods"
  {:semantic (semantic-clustering documents)
   :temporal (temporal-clustering documents)  
   :structural (structural-clustering documents)
   :complexity (complexity-clustering documents)
   :hybrid (hybrid-clustering documents)
   :adaptive (dynamic-reclustering documents 0.3)})

(defn cluster-similarity-matrix [clusters]
  "Calculate inter-cluster similarity for smooth transitions"
  (let [cluster-pairs (for [c1 (keys clusters)
                           c2 (keys clusters)
                           :when (not= c1 c2)]
                       [c1 c2])]
    (reduce (fn [matrix [c1 c2]]
              (let [docs1 (get clusters c1)
                    docs2 (get clusters c2)
                    avg-similarity (if (and (seq docs1) (seq docs2))
                                    (/ (reduce + 
                                              (for [d1 docs1 d2 docs2]
                                                (semantic/cosine-similarity 
                                                 (:semantic-vector d1)
                                                 (:semantic-vector d2))))
                                       (* (count docs1) (count docs2)))
                                    0)]
                (assoc-in matrix [c1 c2] avg-similarity)))
            {} cluster-pairs)))

(defn smooth-cluster-transitions [old-clusters new-clusters]
  "Calculate transition animations between clustering states"
  (let [old-docs (set (mapcat val old-clusters))
        new-docs (set (mapcat val new-clusters))
        
        ;; Documents that moved clusters
        moved-docs (set/intersection old-docs new-docs)
        
        ;; Calculate movement vectors for animation
        movements (reduce (fn [moves doc]
                           (let [old-cluster (first (keep (fn [[k v]] 
                                                          (when (some #(= % doc) v) k))
                                                         old-clusters))
                                new-cluster (first (keep (fn [[k v]]
                                                         (when (some #(= % doc) v) k))
                                                        new-clusters))]
                             (if (not= old-cluster new-cluster)
                               (conj moves {:doc doc 
                                          :from old-cluster 
                                          :to new-cluster})
                               moves)))
                         [] moved-docs)]
    {:movements movements
     :stable-docs (set/difference old-docs (set (map :doc movements)))
     :new-docs (set/difference new-docs old-docs)
     :removed-docs (set/difference old-docs new-docs)}))