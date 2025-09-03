#lang racket

;; Silver Lining: Experimental Semantic Clustering & Advanced UI
;; Port 44502 - The Laboratory of Ideas

(require web-server/servlet-env
         web-server/http
         xml
         net/url
         net/uri-codec
         math/statistics
         racket/hash
         racket/set)

;; Advanced State - Semantic Knowledge Graph
(define *essays* (make-hash))
(define *semantic-vectors* (make-hash))
(define *concept-clusters* (make-hash))
(define *intermediate-reps* (make-hash))
(define *port* 44502)

;; Linguistic Analysis - Extract Semantic Features
(define (extract-concepts text)
  "Extract key concepts using frequency and contextual analysis"
  (define words (regexp-split #rx"[^a-zA-Z0-9-]+" (string-downcase text)))
  (define filtered (filter (λ (w) (> (string-length w) 3)) words))
  (define word-freq (make-hash))
  
  ;; Build frequency map
  (for ([word filtered])
    (hash-set! word-freq word (add1 (hash-ref word-freq word 0))))
  
  ;; Extract high-frequency concepts
  (define concepts 
    (filter (λ (pair) (>= (cdr pair) 2))
            (hash->list word-freq)))
  
  ;; Add contextual concepts (words that appear together)
  (define bigrams 
    (for/list ([i (in-range (sub1 (length filtered)))])
      (string-append (list-ref filtered i) "-" (list-ref filtered (add1 i)))))
  
  (append (map car concepts) bigrams))

;; Semantic Vector Space - TF-IDF with Concept Weighting  
(define (create-semantic-vector text concepts)
  "Create weighted semantic vector with concept importance"
  (define all-words (regexp-split #rx"[^a-zA-Z0-9-]+" (string-downcase text)))
  (define concept-weights (make-hash))
  
  ;; Base TF weighting
  (for ([concept concepts])
    (define tf (length (filter (λ (w) (string-contains? w concept)) all-words)))
    (when (> tf 0)
      (hash-set! concept-weights concept (* tf (log (+ 1 tf))))))
  
  ;; Boost philosophical and technical concepts
  (define boost-patterns 
    '(("think" . 1.5) ("system" . 1.3) ("complex" . 1.4) ("simple" . 1.4)
      ("technology" . 1.3) ("human" . 1.2) ("question" . 1.3) ("understand" . 1.4)))
  
  (for ([pattern boost-patterns])
    (define concept (car pattern))
    (define multiplier (cdr pattern))
    (when (hash-has-key? concept-weights concept)
      (hash-set! concept-weights concept 
                 (* (hash-ref concept-weights concept) multiplier))))
  
  concept-weights)

;; Advanced Similarity - Multiple Metrics
(define (calculate-semantic-similarity vec1 vec2)
  "Multi-dimensional semantic similarity with concept overlap weighting"
  (define all-concepts (set->list (set-union (list->set (hash-keys vec1))
                                             (list->set (hash-keys vec2)))))
  
  (if (empty? all-concepts) 0
      (let ([dot-product 0.0]
            [norm1 0.0]
            [norm2 0.0]
            [concept-overlap 0])
        
        ;; Compute cosine similarity
        (for ([concept all-concepts])
          (define w1 (hash-ref vec1 concept 0))
          (define w2 (hash-ref vec2 concept 0))
          (set! dot-product (+ dot-product (* w1 w2)))
          (set! norm1 (+ norm1 (* w1 w1)))
          (set! norm2 (+ norm2 (* w2 w2)))
          (when (and (> w1 0) (> w2 0))
            (set! concept-overlap (add1 concept-overlap))))
        
        (define cosine-sim (if (or (= norm1 0) (= norm2 0)) 0
                              (/ dot-product (* (sqrt norm1) (sqrt norm2)))))
        
        ;; Weight by concept overlap ratio
        (define overlap-weight (/ concept-overlap (max 1 (length all-concepts))))
        
        ;; Combine metrics
        (+ (* 0.7 cosine-sim) (* 0.3 overlap-weight)))))

;; Clustering Algorithm - Hierarchical with Semantic Grouping
(define (create-semantic-clusters)
  "Create multi-level semantic clusters using concept analysis"
  (define clusters (make-hash))
  (define essays-list (hash->list *essays*))
  
  ;; Level 1: Concept-based clustering
  (for ([essay-pair essays-list])
    (define path (car essay-pair))
    (define content (cdr essay-pair))
    (define concepts (extract-concepts content))
    
    ;; Determine primary cluster by dominant concepts
    (define cluster-key
      (cond
        [(ormap (λ (c) (string-contains? c "technolog")) concepts) "technology"]
        [(ormap (λ (c) (or (string-contains? c "simple") 
                           (string-contains? c "complex"))) concepts) "complexity"]  
        [(ormap (λ (c) (or (string-contains? c "think")
                           (string-contains? c "question")
                           (string-contains? c "understand"))) concepts) "philosophy"]
        [(ormap (λ (c) (string-contains? c "human")) concepts) "humanity"]
        [else "general"]))
    
    (hash-set! clusters cluster-key 
               (cons essay-pair (hash-ref clusters cluster-key '()))))
  
  ;; Level 2: Similarity-based sub-clustering within each group
  (define refined-clusters (make-hash))
  (hash-map clusters
    (λ (cluster-name essays)
      (if (<= (length essays) 2)
          (hash-set! refined-clusters cluster-name essays)
          ;; Further subdivide large clusters by similarity
          (let ([sub-clusters (subdivide-by-similarity essays 0.3)])
            (for ([i (in-range (length sub-clusters))])
              (define sub-name (string-append cluster-name "-" (number->string (add1 i))))
              (hash-set! refined-clusters sub-name (list-ref sub-clusters i)))))))
  
  refined-clusters)

(define (subdivide-by-similarity essays threshold)
  "Subdivide essay group by semantic similarity threshold"
  (define sub-clusters '())
  (for ([essay essays])
    (define path (car essay))
    (define vector (hash-ref *semantic-vectors* path))
    (define assigned #f)
    
    ;; Try to assign to existing sub-cluster
    (for ([cluster sub-clusters] #:when (not assigned))
      (define representative (caar cluster))
      (define rep-vector (hash-ref *semantic-vectors* representative))
      (when (> (calculate-semantic-similarity vector rep-vector) threshold)
        (set! cluster (cons essay cluster))
        (set! assigned #t)))
    
    ;; Create new sub-cluster if no match
    (when (not assigned)
      (set! sub-clusters (cons (list essay) sub-clusters))))
  
  sub-clusters)

;; Intermediate Representations - Multi-Modal Essay Analysis
(define (create-intermediate-representation path content)
  "Create rich intermediate representation with multiple analytical views"
  (define concepts (extract-concepts content))
  (define sentences (regexp-split #rx"[.!?]+" content))
  (define paragraphs (filter non-empty-string? (regexp-split #rx"\n\n+" content)))
  
  (hash 'concepts concepts
        'sentence-count (length sentences)
        'paragraph-count (length paragraphs)
        'word-count (length (regexp-split #rx"\\s+" content))
        'complexity-score (calculate-complexity-score content)
        'emotional-tone (analyze-emotional-tone content)
        'key-phrases (extract-key-phrases content)
        'structural-pattern (analyze-structure content)))

(define (calculate-complexity-score text)
  "Estimate cognitive complexity using multiple metrics"
  (define sentences (regexp-split #rx"[.!?]+" text))
  (define avg-sentence-length (if (empty? sentences) 0
                                  (/ (string-length text) (length sentences))))
  (define unique-words (set-count (list->set (regexp-split #rx"\\s+" (string-downcase text)))))
  (define total-words (length (regexp-split #rx"\\s+" text)))
  (define lexical-diversity (if (= total-words 0) 0 (/ unique-words total-words)))
  
  ;; Combine metrics (normalized to 0-1 range)
  (min 1.0 (+ (* 0.3 (min 1.0 (/ avg-sentence-length 50)))
              (* 0.4 lexical-diversity)
              (* 0.3 (min 1.0 (/ unique-words 200))))))

(define (analyze-emotional-tone text)
  "Basic emotional tone analysis using keyword patterns"
  (define positive-words '("good" "great" "beautiful" "love" "joy" "hope" "amazing" "wonderful"))
  (define negative-words '("bad" "terrible" "hate" "fear" "anger" "sad" "difficult" "problem"))
  (define contemplative-words '("think" "consider" "reflect" "ponder" "question" "perhaps" "maybe"))
  
  (define words (regexp-split #rx"[^a-zA-Z]+" (string-downcase text)))
  (define pos-count (length (filter (λ (w) (member w positive-words)) words)))
  (define neg-count (length (filter (λ (w) (member w negative-words)) words)))
  (define cont-count (length (filter (λ (w) (member w contemplative-words)) words)))
  
  (cond
    [(> cont-count (max pos-count neg-count)) "contemplative"]
    [(> pos-count neg-count) "positive"]
    [(> neg-count pos-count) "critical"]
    [else "neutral"]))

(define (extract-key-phrases content)
  "Extract significant phrases using pattern matching"
  (define phrases (regexp-match* #rx"[A-Z][^.!?]*[.!?]" content))
  (filter (λ (phrase) (> (string-length phrase) 20)) phrases))

(define (analyze-structure content)
  "Analyze essay structural patterns"
  (cond
    [(regexp-match #rx"## " content) "sectioned"]
    [(regexp-match #rx"[0-9]+\\. " content) "enumerated"]  
    [(regexp-match #rx"- " content) "listed"]
    [(> (length (regexp-split #rx"\n\n" content)) 5) "narrative"]
    [else "simple"]))

;; Enhanced HTML Generation with Experimental UI
(define (experimental-page-wrapper title body)
  (response/xexpr
   `(html 
     (head (title ,title)
           (meta ((charset "utf-8")))
           (link ((rel "preconnect") (href "https://fonts.googleapis.com")))
           (link ((rel "preconnect") (href "https://fonts.gstatic.com") (crossorigin "")))
           (link ((rel "stylesheet") (href "https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,400;0,600;1,400&family=Fira+Code:wght@400;500&family=Inter+Tight:wght@300;400;500;600&family=Crimson+Text:wght@400;600&display=swap")))
           (style "
             :root {
               --complexity-low: #e8f5e8;
               --complexity-med: #fff3cd;
               --complexity-high: #f8d7da;
               --tone-positive: #d4edda;
               --tone-negative: #f8d7da;
               --tone-contemplative: #e2e3f5;
               --tone-neutral: #f8f9fa;
               --cluster-tech: #667eea;
               --cluster-phil: #764ba2;
               --cluster-humanity: #f093fb;
               --cluster-complexity: #f68084;
               --cluster-general: #4ecdc4;
             }
             
             body { 
               font-family: 'Crimson Text', 'Vollkorn', serif; 
               max-width: 1200px; margin: 0 auto; padding: 2rem; line-height: 1.8;
               background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
               color: #e0e0e0; }
             
             .experimental-grid { display: grid; grid-template-columns: 300px 1fr 250px; gap: 2rem; }
             
             .cluster-nav { background: rgba(255,255,255,0.03); padding: 1.5rem; 
                           border-radius: 12px; border-left: 4px solid var(--cluster-tech); }
             
             .cluster-item { margin-bottom: 1rem; padding: 0.8rem; background: rgba(255,255,255,0.05);
                            border-radius: 8px; cursor: pointer; transition: all 0.3s ease; }
             
             .cluster-item:hover { background: rgba(255,255,255,0.1); transform: translateX(5px); }
             
             .main-content { background: rgba(255,255,255,0.02); padding: 2rem; border-radius: 12px; }
             
             .essay-card { background: rgba(255,255,255,0.04); padding: 1.8rem; margin: 1.5rem 0;
                          border-radius: 12px; border-left: 4px solid transparent; 
                          transition: all 0.4s ease; position: relative; overflow: hidden; }
             
             .essay-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0;
                                  height: 3px; background: linear-gradient(90deg, transparent, 
                                  var(--accent-color, #667eea), transparent); }
             
             .essay-card:hover { transform: translateY(-5px); 
                                background: rgba(255,255,255,0.06); 
                                box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
             
             .meta-panel { background: rgba(255,255,255,0.03); padding: 1.5rem; 
                          border-radius: 12px; font-size: 0.9em; }
             
             .complexity-indicator { display: inline-block; width: 12px; height: 12px; 
                                    border-radius: 50%; margin-right: 0.5rem; }
             
             .tone-badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 12px;
                          font-size: 0.8em; margin-right: 0.5rem; }
             
             .concept-cloud { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }
             
             .concept-tag { background: rgba(102, 126, 234, 0.2); color: #a8b5ff; 
                           padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8em; }
             
             h1 { color: #ff6b9d; text-align: center; margin: 2rem 0; 
                  font-family: 'Inter Tight', sans-serif; }
             
             h2 { color: #c44569; font-family: 'Inter Tight', sans-serif; }
             
             h3 { color: #f8b500; font-family: 'Inter Tight', sans-serif; }
             
             .essay-title { font-size: 1.3em; margin-bottom: 1rem; color: #ffeaa7; 
                           font-family: 'Inter Tight', sans-serif; font-weight: 500; }
             
             .similarity-links { margin-top: 1rem; padding-top: 1rem; 
                                border-top: 1px solid rgba(255,255,255,0.1); }
             
             .similarity-link { color: #74b9ff; text-decoration: none; margin-right: 1rem;
                               font-size: 0.9em; }
             
             .similarity-link:hover { text-decoration: underline; }
             
             .structural-pattern { font-style: italic; color: #a0a0a0; font-size: 0.8em; }
             
             @media (max-width: 1024px) {
               .experimental-grid { grid-template-columns: 1fr; }
               .cluster-nav, .meta-panel { order: -1; }
             }
           "))
     (body ,@body))))

;; Discovery with Enhanced Analysis
(define (discover-essays-advanced)
  (define cmd "find /home/uprootiny/essays -name '*.md' | head -50")
  (define paths (string-split (with-output-to-string 
                               (λ () (system cmd))) "\n"))
  (for ([path (filter non-empty-string? paths)])
    (when (file-exists? path)
      (printf "🔬 Analyzing: ~a\n" path)
      (define content (with-input-from-file path
                        (λ () (port->string (current-input-port)))))
      (hash-set! *essays* path content)
      
      ;; Create semantic analysis
      (define concepts (extract-concepts content))
      (hash-set! *semantic-vectors* path (create-semantic-vector content concepts))
      (hash-set! *intermediate-reps* path (create-intermediate-representation path content))))
  
  ;; Generate clusters after all essays are analyzed
  (set! *concept-clusters* (create-semantic-clusters))
  (printf "📊 Generated ~a semantic clusters\n" (hash-count *concept-clusters*)))

;; Enhanced Index Page with Clustering
(define (experimental-index-page)
  (experimental-page-wrapper "🧪 Silver Lining Laboratory"
    `((div ((class "experimental-grid"))
           
           ;; Cluster Navigation
           (div ((class "cluster-nav"))
                (h3 "🧠 Semantic Clusters")
                ,@(hash-map *concept-clusters*
                    (λ (cluster-name essays)
                      `(div ((class "cluster-item") 
                             (style ,(format "border-left-color: var(--cluster-~a)" 
                                           (car (string-split cluster-name "-")))))
                            (strong ,cluster-name)
                            (div ,(format "(~a essays)" (length essays)))))))
           
           ;; Main Content
           (div ((class "main-content"))
                (h1 "🧪 Experimental Essay Laboratory")
                (p "Advanced semantic clustering with intermediate representations")
                (div ((class "essay-collection"))
                     ,@(hash-map *essays* 
                         (λ (path content)
                           (define ir (hash-ref *intermediate-reps* path))
                           (define concepts (hash-ref ir 'concepts '()))
                           (define complexity (hash-ref ir 'complexity-score 0))
                           (define tone (hash-ref ir 'emotional-tone "neutral"))
                           (define structure (hash-ref ir 'structural-pattern "simple"))
                           
                           `(div ((class "essay-card")
                                  (style ,(format "--accent-color: var(--cluster-~a)" 
                                                (if (string-contains? (string-downcase content) "technology")
                                                    "tech" "general"))))
                                 (div ((class "essay-title"))
                                      (a ((href ,(format "/essay/~a" (uri-encode path))))
                                         ,(path->string (file-name-from-path path))))
                                 
                                 ;; Metadata indicators
                                 (div ((style "margin: 0.5rem 0;"))
                                      (span ((class "complexity-indicator")
                                             (style ,(format "background: ~a" 
                                                           (cond [(< complexity 0.3) "var(--complexity-low)"]
                                                                 [(< complexity 0.6) "var(--complexity-med)"]
                                                                 [else "var(--complexity-high)"])))))
                                      (span ((class "tone-badge")
                                             (style ,(format "background: var(--tone-~a); color: #333" tone)))
                                            ,tone)
                                      (span ((class "structural-pattern")) ,structure))
                                 
                                 ;; Concept cloud
                                 (div ((class "concept-cloud"))
                                      ,@(take (hash-ref ir 'concepts '()) (min 5 (length concepts)))
                                      (map (λ (concept) 
                                             `(span ((class "concept-tag")) ,concept))))
                                 
                                 ;; Content preview
                                 (p ,(substring content 0 (min 200 (string-length content))))
                                 
                                 ;; Similarity links
                                 (div ((class "similarity-links"))
                                      "🔗 Related: "
                                      ,@(find-similar-essays path 3)))))))
           
           ;; Meta Panel
           (div ((class "meta-panel"))
                (h4 "📊 Collection Stats")
                (p ,(format "~a essays analyzed" (hash-count *essays*)))
                (p ,(format "~a semantic clusters" (hash-count *concept-clusters*)))
                (p ,(format "~a unique concepts" (count-unique-concepts)))
                
                (h4 "🎛️ Analysis Modes")
                (div "• Semantic clustering")
                (div "• Complexity scoring")
                (div "• Emotional tone detection")
                (div "• Structural pattern analysis"))))))

(define (find-similar-essays current-path limit)
  "Find most similar essays using semantic vectors"
  (define current-vector (hash-ref *semantic-vectors* current-path))
  (define similarities
    (hash-map *semantic-vectors*
      (λ (path vector)
        (if (equal? path current-path) 
            (cons path 0)
            (cons path (calculate-semantic-similarity current-vector vector))))))
  
  (define sorted-similarities 
    (take (sort similarities (λ (a b) (> (cdr a) (cdr b)))) 
          (min limit (sub1 (length similarities)))))
  
  (map (λ (sim-pair)
         (define path (car sim-pair))
         (define score (cdr sim-pair))
         `(a ((class "similarity-link") 
              (href ,(format "/essay/~a" (uri-encode path))))
             ,(format "~a (~a%)" 
                     (path->string (file-name-from-path path))
                     (inexact->exact (round (* 100 score))))))
       sorted-similarities))

(define (count-unique-concepts)
  (define all-concepts (set))
  (hash-map *intermediate-reps*
    (λ (path ir)
      (set! all-concepts (set-union all-concepts 
                                    (list->set (hash-ref ir 'concepts '()))))))
  (set-count all-concepts))

;; Enhanced Essay View with Analysis
(define (experimental-essay-page path-encoded)
  (define path (uri-decode path-encoded))
  (define content (hash-ref *essays* path #f))
  (if content
      (let ([name (path->string (file-name-from-path path))]
            [ir (hash-ref *intermediate-reps* path)]
            [lines (string-split content "\n")])
        (experimental-page-wrapper name
          `((a ((class "back") (href "/")) "← Laboratory")
            (h1 ,name)
            
            ;; Analysis panel
            (div ((style "background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; margin: 1rem 0;"))
                 (h3 "🔬 Analysis")
                 (div ,(format "Complexity: ~a/1.0" (real->decimal-string (hash-ref ir 'complexity-score 0) 2)))
                 (div ,(format "Tone: ~a" (hash-ref ir 'emotional-tone "unknown")))  
                 (div ,(format "Structure: ~a" (hash-ref ir 'structural-pattern "unknown")))
                 (div ,(format "Word count: ~a" (hash-ref ir 'word-count 0))))
            
            (div ((class "essay-text"))
                 ,@(map (λ (line) 
                          (cond 
                            [(string-prefix? line "# ") `(h1 ,(substring line 2))]
                            [(string-prefix? line "## ") `(h2 ,(substring line 3))]
                            [(string-prefix? line "### ") `(h3 ,(substring line 4))]
                            [(non-empty-string? line) `(p ,line)]
                            [else `(br)]))
                        lines))
            
            ;; Similar essays
            (div ((style "margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);"))
                 (h3 "🌸 Semantically Similar")
                 (div ,@(find-similar-essays path 5))))))
      (experimental-page-wrapper "Not Found" 
        '((h1 "Essay not found in the laboratory")
          (a ((class "back") (href "/")) "← Back to Laboratory")))))

;; Router for experimental features
(define (experimental-app req)
  (define path-segments (map path/param-path (url-path (request-uri req))))
  (match path-segments
    ['("") (experimental-index-page)]
    [(list "essay" path-encoded) (experimental-essay-page path-encoded)]
    [_ (experimental-page-wrapper "Not Found" '((h1 "Path not found")))]))

;; Enhanced Startup
(define (start-experimental)
  (printf "🧪 Initializing Experimental Silver Lining Laboratory...\n")
  (discover-essays-advanced)
  (printf "📊 Semantic analysis complete\n")
  (printf "🚀 Laboratory serving at http://localhost:~a\n" *port*)
  (serve/servlet experimental-app
                 #:port *port*
                 #:listen-ip "0.0.0.0"
                 #:servlet-regexp #rx""
                 #:servlet-path "/"))

(module+ main (start-experimental))