#lang racket

;; Silver Lining: A Terse Essay Reader in Racket
;; Port 44501 - The Secret Level, The Inverted Garden

(require web-server/servlet-env
         web-server/dispatchers/dispatch
         web-server/http
         web-server/http/response-structs
         web-server/formlets
         xml
         net/url
         net/uri-codec
         json)

;; --- The Essence ---

(define *essays* (make-hash))
(define *vectors* (make-hash))
(define *port* 44501)

;; Unix -> Web: The Minimal Path
(define (slurp path)
  (with-input-from-file path
    (λ () (port->string (current-input-port)))))

(define (discover-essays [root "/home/uprootiny"])
  (define cmd (format "find ~a -name '*.md' -not -path '*/.*' -not -path '*/node_modules/*'" root))
  (define paths (string-split (with-output-to-string (λ () (system cmd))) "\n"))
  (for ([path (filter non-empty-string? paths)])
    (when (file-exists? path)
      (hash-set! *essays* path (slurp path)))))

;; Word Vectors: Minimal TF-IDF 
(define (words->vector text)
  (define words (regexp-split #rx"[^a-zA-Z0-9]+" (string-downcase text)))
  (define filtered (filter (λ (w) (> (string-length w) 3)) words))
  (define counts (make-hash))
  (for ([w filtered]) 
    (hash-set! counts w (add1 (hash-ref counts w 0))))
  counts)

(define (cosine-similarity v1 v2)
  (define keys (set-union (list->set (hash-keys v1)) (list->set (hash-keys v2))))
  (define (dot-product)
    (for/sum ([k keys])
      (* (hash-ref v1 k 0) (hash-ref v2 k 0))))
  (define (magnitude v)
    (sqrt (for/sum ([k keys]) (expt (hash-ref v k 0) 2))))
  (define mag1 (magnitude v1))
  (define mag2 (magnitude v2))
  (if (or (= mag1 0) (= mag2 0)) 0
      (/ (dot-product) (* mag1 mag2))))

;; The Garden of Similarity
(define (find-similar path [limit 5])
  (define target-vec (hash-ref *vectors* path #f))
  (if (not target-vec) '()
      (take (sort 
             (filter (λ (p) (not (equal? path (first p))))
                     (for/list ([(p v) *vectors*])
                       (list p (cosine-similarity target-vec v))))
             (λ (a b) (> (second a) (second b))))
            (min limit (sub1 (hash-count *vectors*))))))

;; HTML Essence
(define (page-wrapper title body)
  `(html 
    (head (meta ((charset "utf-8")))
          (title ,title)
          (style "
            body { font-family: Georgia, serif; line-height: 1.6; 
                   max-width: 800px; margin: 0 auto; padding: 2rem;
                   background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                   color: #eee; }
            .header { text-align: center; margin: 3rem 0; }
            .essay { background: rgba(255,255,255,0.05); padding: 2rem; 
                     border-radius: 8px; margin: 1rem 0; }
            .similar { opacity: 0.7; font-size: 0.9em; margin-top: 1rem; }
            .similar a { color: #8cc8ff; text-decoration: none; }
            .similar a:hover { text-decoration: underline; }
            a { color: #ff6b6b; }
            pre { background: rgba(0,0,0,0.3); padding: 1rem; overflow-x: auto; }
            h1 { color: #ff9ff3; }
            h2 { color: #54a0ff; }
            h3 { color: #5f27cd; }
            .path { font-family: monospace; opacity: 0.5; font-size: 0.8em; }
            .garden { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }
            .seed { background: rgba(255,255,255,0.1); padding: 0.3rem 0.6rem; 
                    border-radius: 12px; font-size: 0.8em; }
          "))
    (body ,@body)))

(define (index-page)
  (page-wrapper "Silver Lining - Essay Garden"
    `((div ((class "header"))
           (h1 "🌙 Silver Lining")
           (p "The Secret Level - Essays in Harmonized Chaos")
           (div ((class "path")) ,(format "~a essays discovered" (hash-count *essays*))))
      
      (div ((class "garden"))
           ,@(for/list ([(path content) *essays*])
               (define name (path->string (file-name-from-path path)))
               `(a ((href ,(format "/essay?path=~a" (uri-encode path)))
                    (class "seed"))
                   ,name))))))

(define (essay-page path-str)
  (define path (uri-decode path-str))
  (define content (hash-ref *essays* path #f))
  (if (not content)
      (page-wrapper "Not Found" '((h1 "Essay not found in the garden")))
      (let* ([name (path->string (file-name-from-path path))]
             [similar (find-similar path)]
             [lines (string-split content "\n")]
             [paragraphs (filter non-empty-string? lines)])
        (page-wrapper name
          `((div ((class "essay"))
                 (h1 ,name)
                 (div ((class "path")) ,path)
                 ,@(map (λ (p) `(p ,p)) paragraphs)
                 
                 ,(if (empty? similar) ""
                      `(div ((class "similar"))
                            (h3 "🌸 Resonant Essays")
                            (ul ,@(for/list ([s similar])
                                    `(li (a ((href ,(format "/essay?path=~a" 
                                                            (uri-encode (first s)))))
                                            ,(path->string (file-name-from-path (first s))))
                                         ,(format " (~a%)" (inexact->exact 
                                                           (round (* 100 (second s))))))))))))))))

;; The Dispatcher - Minimal Routing
(define (dispatch req)
  (define path (url-path (request-uri req)))
  (define segments (map path/param-path path))
  
  (cond
    [(equal? segments '("")) 
     (response/xexpr (index-page))]
    
    [(equal? segments '("essay"))
     (define query (url-query (request-uri req)))
     (define path-param (and query (assq 'path query)))
     (if path-param
         (response/xexpr (essay-page (cdr path-param)))
         (response/xexpr (page-wrapper "Error" '((h1 "No path specified")))))]
    
    [else (response 404 #"Not Found" (current-seconds) #"text/plain" '() #f)])))

;; The Awakening
(define (initialize)
  (printf "🌙 Discovering essays in the ontological garden...\n")
  (discover-essays)
  (printf "📚 Found ~a essays\n" (hash-count *essays*))
  
  (printf "🧠 Computing semantic vectors...\n")
  (for ([(path content) *essays*])
    (hash-set! *vectors* path (words->vector content)))
  (printf "✨ Vector space ready\n"))

(define (start-server)
  (initialize)
  (printf "🚀 Silver Lining serving at http://localhost:~a\n" *port*)
  (serve/servlet dispatch
                 #:port *port*
                 #:servlet-regexp #rx""
                 #:servlet-path "/"))

;; The Invocation
(module+ main
  (start-server))