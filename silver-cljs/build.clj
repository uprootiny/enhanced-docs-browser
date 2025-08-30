(require '[cljs.build.api :as b])

(b/build "src/cljs"
  {:main 'silver.core
   :output-to "resources/public/js/compiled/main.js"
   :output-dir "resources/public/js/compiled"
   :asset-path "/js/compiled"
   :optimizations :none
   :source-map-timestamp true})

(println "ClojureScript build completed!")