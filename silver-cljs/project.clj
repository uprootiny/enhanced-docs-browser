(defproject silver-lining "0.1.0"
  :description "Smooth ClojureScript documentation explorer with live clustering"
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/clojurescript "1.11.60"]
                 [reagent "1.2.0"]
                 [re-frame "1.3.0"]
                 [cljs-ajax "0.8.4"]
                 [day8.re-frame/http-fx "0.2.4"]
                 [binaryage/devtools "1.0.6"]
                 [thheller/shadow-cljs "2.20.0"]]
  
  :min-lein-version "2.9.0"
  
  :source-paths ["src/clj" "src/cljs"]
  
  :clean-targets ^{:protect false} ["resources/public/js/compiled" "target"]
  
  :profiles
  {:dev {:dependencies [[cider/piggieback "0.5.3"]]
         :repl-options {:nrepl-middleware [cider.piggieback/wrap-cljs-repl]}}})