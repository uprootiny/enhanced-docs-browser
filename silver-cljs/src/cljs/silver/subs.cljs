(ns silver.subs
  (:require [re-frame.core :as rf]))

;; Basic data subscriptions
(rf/reg-sub :documents #(:documents %))
(rf/reg-sub :loading? #(:loading? %))
(rf/reg-sub :search-query #(:search-query %))
(rf/reg-sub :clusters #(:clusters %))
(rf/reg-sub :selected-clusters #(:selected-clusters %))
(rf/reg-sub :complexity-filter #(:complexity-filter %))
(rf/reg-sub :tone-filter #(:tone-filter %))
(rf/reg-sub :clustering-method #(:clustering-method %))
(rf/reg-sub :view-mode #(:view-mode %))
(rf/reg-sub :selected-document #(:selected-document %))
(rf/reg-sub :live-suggestions #(:live-suggestions %))
(rf/reg-sub :similarity-threshold #(:similarity-threshold %))

;; Computed subscriptions
(rf/reg-sub
 :filtered-document-count
 :<- [:documents]
 (fn [documents _]
   (count documents)))

(rf/reg-sub
 :cluster-stats
 :<- [:clusters]
 (fn [clusters _]
   (reduce (fn [acc [cluster-id docs]]
             (assoc acc cluster-id {:count (count docs)
                                   :avg-complexity (/ (reduce + (map :complexity docs)) 
                                                     (max 1 (count docs)))}))
           {} clusters)))

(rf/reg-sub
 :complexity-distribution
 :<- [:documents]
 (fn [documents _]
   (let [complexities (map :complexity documents)]
     {:min (apply min complexities)
      :max (apply max complexities)
      :avg (/ (reduce + complexities) (max 1 (count complexities)))
      :distribution (frequencies (map #(int (* 10 %)) complexities))})))

(rf/reg-sub
 :tone-distribution
 :<- [:documents]
 (fn [documents _]
   (frequencies (map :tone documents))))

(rf/reg-sub
 :live-cluster-updates
 :<- [:documents]
 :<- [:similarity-threshold]
 (fn [[documents threshold] _]
   ;; Real-time clustering as documents/filters change
   (when (seq documents)
     (let [now (js/Date.now)]
       {:timestamp now
        :cluster-count (count (group-by :primary-cluster documents))
        :avg-similarity (/ (reduce + (map :max-similarity documents))
                          (count documents))}))))

(rf/reg-sub
 :search-suggestions
 :<- [:documents]
 :<- [:search-query] 
 (fn [[documents query] _]
   (when (and (seq query) (>= (count query) 2))
     (->> documents
          (mapcat :concepts)
          (filter #(and (string? %)
                       (.includes (.toLowerCase %) (.toLowerCase query))))
          (take 8)
          distinct))))