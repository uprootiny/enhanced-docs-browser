(ns silver.events
  (:require [re-frame.core :as rf]
            [ajax.core :as ajax]
            [silver.semantic :as semantic]
            [silver.clustering :as clustering]))

;; Initial app state
(rf/reg-event-db
 :initialize
 (fn [_ _]
   {:documents []
    :raw-documents []
    :loading? false
    :search-query ""
    :selected-clusters #{}
    :complexity-filter [0 1]
    :tone-filter :all
    :similarity-threshold 0.3
    :clustering-method :semantic
    :view-mode :grid
    :clusters {}
    :semantic-index {}
    :selected-document nil
    :live-suggestions []}))

;; Fetch documents from main server API
(rf/reg-event-fx
 :fetch-documents
 (fn [{:keys [db]} _]
   {:db (assoc db :loading? true)
    :http-xhrio {:method :get
                 :uri "http://localhost:44500/api/files"
                 :format (ajax/json-request-format)
                 :response-format (ajax/json-response-format {:keywords? true})
                 :on-success [:fetch-documents-success]
                 :on-failure [:fetch-documents-failure]}}))

(rf/reg-event-fx
 :fetch-documents-success
 (fn [{:keys [db]} [_ documents]]
   (let [enhanced-docs (map semantic/enhance-document documents)]
     {:db (-> db
              (assoc :loading? false)
              (assoc :raw-documents documents)
              (assoc :documents enhanced-docs)
              (assoc :clusters (clustering/create-clusters enhanced-docs))
              (assoc :semantic-index (semantic/build-index enhanced-docs)))
      :dispatch [:update-live-filtering]})))

(rf/reg-event-db
 :fetch-documents-failure
 (fn [db [_ error]]
   (println "Failed to fetch documents:" error)
   (assoc db :loading? false :error error)))

;; Live search and filtering
(rf/reg-event-fx
 :update-search-query
 (fn [{:keys [db]} [_ query]]
   {:db (assoc db :search-query query)
    :dispatch-later [{:ms 150 :dispatch [:update-live-filtering]}]}))

(rf/reg-event-db
 :update-live-filtering
 (fn [db _]
   (let [{:keys [raw-documents search-query selected-clusters 
                complexity-filter tone-filter similarity-threshold]} db
         enhanced-docs (map semantic/enhance-document raw-documents)
         filtered-docs (semantic/filter-documents enhanced-docs
                                                 search-query
                                                 selected-clusters
                                                 complexity-filter
                                                 tone-filter)
         new-clusters (clustering/dynamic-reclustering filtered-docs similarity-threshold)]
     (-> db
         (assoc :documents filtered-docs)
         (assoc :clusters new-clusters)))))

;; Clustering controls
(rf/reg-event-fx
 :toggle-cluster-filter
 (fn [{:keys [db]} [_ cluster-id]]
   (let [new-selected (if (contains? (:selected-clusters db) cluster-id)
                        (disj (:selected-clusters db) cluster-id)
                        (conj (:selected-clusters db) cluster-id))]
     {:db (assoc db :selected-clusters new-selected)
      :dispatch [:update-live-filtering]})))

(rf/reg-event-fx
 :adjust-complexity-filter
 (fn [{:keys [db]} [_ [min-val max-val]]]
   {:db (assoc db :complexity-filter [min-val max-val])
    :dispatch [:update-live-filtering]}))

(rf/reg-event-fx
 :change-clustering-method
 (fn [{:keys [db]} [_ method]]
   (let [documents (:documents db)
         new-clusters (case method
                        :semantic (clustering/semantic-clustering documents)
                        :temporal (clustering/temporal-clustering documents)
                        :structural (clustering/structural-clustering documents)
                        :hybrid (clustering/hybrid-clustering documents))]
     {:db (-> db
              (assoc :clustering-method method)
              (assoc :clusters new-clusters))
      :dispatch [:update-live-filtering]})))

;; Document selection and similarity
(rf/reg-event-fx
 :select-document
 (fn [{:keys [db]} [_ doc]]
   (let [similar-docs (semantic/find-similar-documents 
                       doc (:documents db) (:similarity-threshold db))]
     {:db (-> db
              (assoc :selected-document doc)
              (assoc :live-suggestions similar-docs))})))

;; Smooth transitions
(rf/reg-event-db
 :set-view-mode
 (fn [db [_ mode]]
   (assoc db :view-mode mode)))

(rf/reg-event-db
 :adjust-similarity-threshold
 (fn [db [_ threshold]]
   (assoc db :similarity-threshold threshold)))