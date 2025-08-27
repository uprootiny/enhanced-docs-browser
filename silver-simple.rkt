#lang racket

;; Silver Lining: The Minimal Essence
;; Port 44501 - Terse Beauty in Motion

(require web-server/servlet-env
         web-server/http
         xml
         net/url
         net/uri-codec)

;; State - The Garden of Essays
(define *essays* (make-hash))
(define *port* 44501)

;; Discovery - Unix to Memory
(define (discover-essays)
  (define cmd "find /home/uprootiny -name '*.md' -not -path '*/.*' -not -path '*/node_modules/*' | head -50")
  (define paths (string-split (with-output-to-string 
                               (λ () (system cmd))) "\n"))
  (for ([path (filter non-empty-string? paths)])
    (when (file-exists? path)
      (printf "Found: ~a\n" path)
      (hash-set! *essays* path 
                 (with-input-from-file path
                   (λ () (port->string (current-input-port))))))))

;; Beauty - Minimal HTML
(define (html-page title body)
  (response/xexpr
   `(html 
     (head (title ,title)
           (meta ((charset "utf-8")))
           (link ((rel "preconnect") (href "https://fonts.googleapis.com")))
           (link ((rel "preconnect") (href "https://fonts.gstatic.com") (crossorigin "")))
           (link ((rel "stylesheet") (href "https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,400;0,600;1,400&family=Fira+Code:wght@400;500&family=Inter+Tight:wght@300;400;500;600&display=swap")))
           (style "
             body { font-family: 'Vollkorn', 'Crimson Text', 'Lora', serif; max-width: 900px; 
                    margin: 0 auto; padding: 2rem; line-height: 1.7;
                    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
                    color: #cccccc; }
             h1 { color: #ff6b9d; text-align: center; margin: 2rem 0; }
             h2 { color: #c44569; }
             h3 { color: #f8b500; }
             .essays { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                      gap: 1rem; margin: 2rem 0; }
             .essay-card { background: rgba(255,255,255,0.05); padding: 1.5rem;
                          border-radius: 8px; border-left: 4px solid #ff6b9d; }
             .essay-card:hover { transform: translateY(-2px); 
                                background: rgba(255,255,255,0.08); }
             .essay-card a { color: #ffeaa7; text-decoration: none; }
             .essay-card a:hover { color: #ff6b9d; }
             .essay-text { background: rgba(0,0,0,0.2); padding: 2rem;
                          border-radius: 8px; margin: 2rem 0; }
             .back { color: #74b9ff; text-decoration: none; }
             .back:hover { text-decoration: underline; }
             pre { background: rgba(0,0,0,0.4); padding: 1rem; overflow-x: auto; 
                   font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace; }
             code { font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace; }
             .essay-card h3 { font-family: 'Inter Tight', sans-serif; font-weight: 500; }
           "))
     (body ,@body))))

;; Index - The Garden View
(define (index-page)
  (html-page "🌙 Silver Lining"
    `((h1 "Silver Lining - The Essay Garden")
      (p ,(format "~a essays in the ontological garden" (hash-count *essays*)))
      (div ((class "essays"))
           ,@(for/list ([(path content) *essays*])
               (define name (path->string (file-name-from-path path)))
               (define preview (string-append 
                               (substring content 0 (min 200 (string-length content)))
                               "..."))
               `(div ((class "essay-card"))
                     (h3 (a ((href ,(format "/essay/~a" (uri-encode path))))
                            ,name))
                     (p ,preview)))))))

;; Essay View - The Reading Experience  
(define (essay-page path-encoded)
  (define path (uri-decode path-encoded))
  (define content (hash-ref *essays* path #f))
  (if content
      (let ([name (path->string (file-name-from-path path))]
            [lines (string-split content "\n")])
        (html-page name
          `((a ((class "back") (href "/")) "← Back to Garden")
            (h1 ,name)
            (div ((class "essay-text"))
                 ,@(map (λ (line) 
                          (cond 
                            [(string-prefix? line "# ") `(h1 ,(substring line 2))]
                            [(string-prefix? line "## ") `(h2 ,(substring line 3))]
                            [(string-prefix? line "### ") `(h3 ,(substring line 4))]
                            [(non-empty-string? line) `(p ,line)]
                            [else `(br)]))
                        lines)))))
      (html-page "Not Found" 
        '((h1 "Essay not found in the garden")
          (a ((class "back") (href "/")) "← Back to Garden")))))

;; Router - The Path Dispatcher
(define (app req)
  (define path-segments (map path/param-path (url-path (request-uri req))))
  (match path-segments
    ['("") (index-page)]
    [(list "essay" path-encoded) (essay-page path-encoded)]
    [_ (html-page "Not Found" '((h1 "Path not found")))]))

;; The Invocation - Awaken the Server
(define (start)
  (printf "🌙 Discovering essays...\n")
  (discover-essays)
  (printf "✨ Found ~a essays\n" (hash-count *essays*))
  (printf "🚀 Silver Lining serving at http://localhost:~a\n" *port*)
  (serve/servlet app
                 #:port *port*
                 #:servlet-regexp #rx""
                 #:servlet-path "/"))

(module+ main (start))