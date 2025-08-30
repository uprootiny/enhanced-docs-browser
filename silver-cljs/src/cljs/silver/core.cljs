(ns silver.core
  (:require [reagent.core :as r]
            [reagent.dom :as rdom]
            [re-frame.core :as rf]
            [ajax.core :as ajax]
            [day8.re-frame.http-fx]
            [silver.events]
            [silver.subs]
            [silver.views :as views]))

;; Enable devtools in development
(when ^boolean js/goog.DEBUG
  (enable-console-print!)
  (println "Silver Lining ClojureScript initializing..."))

(defn ^:export init []
  (println "🌙 Initializing Silver Lining CLJS...")
  (rf/dispatch-sync [:initialize])
  (rf/dispatch [:fetch-documents])
  (rdom/render [views/main-app] (.getElementById js/document "app"))
  (println "✨ Silver Lining ready"))