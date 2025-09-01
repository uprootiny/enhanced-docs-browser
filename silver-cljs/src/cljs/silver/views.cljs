(ns silver.views
  (:require [reagent.core :as r]
            [re-frame.core :as rf]))

(defn smooth-range-slider [value min-val max-val on-change label]
  "Smooth animated range slider with live updates"
  [:div.range-control
   [:label.range-label label]
   [:input {:type "range"
            :min min-val
            :max max-val  
            :step 0.01
            :value value
            :on-input #(on-change (js/parseFloat (.. % -target -value)))
            :class "smooth-slider"}]
   [:span.range-value (str (.toFixed value 2))]])

(defn dual-range-slider [[min-val max-val] range-min range-max on-change label]
  "Dual-handle range slider for filtering ranges"
  (let [local-min (r/atom min-val)
        local-max (r/atom max-val)]
    (fn [[min-val max-val] range-min range-max on-change label]
      [:div.dual-range-control
       [:label.range-label label]
       [:div.dual-range-container
        [:input {:type "range"
                 :min range-min
                 :max range-max
                 :step 0.01
                 :value @local-min
                 :on-input #(let [new-min (js/parseFloat (.. % -target -value))]
                             (when (<= new-min @local-max)
                               (reset! local-min new-min)
                               (on-change [new-min @local-max])))
                 :class "range-min"}]
        [:input {:type "range"
                 :min range-min  
                 :max range-max
                 :step 0.01
                 :value @local-max
                 :on-input #(let [new-max (js/parseFloat (.. % -target -value))]
                             (when (>= new-max @local-min)
                               (reset! local-max new-max)
                               (on-change [@local-min new-max])))
                 :class "range-max"}]]
       [:div.range-values 
        [:span (.toFixed @local-min 2)] 
        [:span " — "] 
        [:span (.toFixed @local-max 2)]]])))

(defn live-search-box []
  "Smooth search with live suggestions and debouncing"
  (let [query @(rf/subscribe [:search-query])
        suggestions @(rf/subscribe [:search-suggestions])]
    [:div.live-search-container
     [:div.search-box
      [:input.search-input 
       {:type "text"
        :placeholder "Search concepts, ideas, themes..."
        :value query
        :on-change #(rf/dispatch [:update-search-query (.. % -target -value)])
        :auto-complete "off"}]
      [:div.search-icon "🔍"]]
     
     (when (seq suggestions)
       [:div.search-suggestions
        (for [suggestion suggestions]
          ^{:key suggestion}
          [:div.suggestion-item
           {:on-click #(rf/dispatch [:update-search-query suggestion])}
           suggestion])])]))

(defn cluster-control-panel []
  "Interactive clustering controls with smooth transitions" 
  (let [clusters @(rf/subscribe [:clusters])
        selected @(rf/subscribe [:selected-clusters])
        method @(rf/subscribe [:clustering-method])
        complexity-filter @(rf/subscribe [:complexity-filter])
        similarity-threshold @(rf/subscribe [:similarity-threshold])]
    
    [:div.cluster-panel
     [:h3.panel-title "🧠 Live Clustering"]
     
     ;; Clustering method selector
     [:div.clustering-methods
      (for [method-option [:semantic :temporal :structural :complexity :hybrid :adaptive]]
        ^{:key method-option}
        [:button.method-button
         {:class (when (= method method-option) "active")
          :on-click #(rf/dispatch [:change-clustering-method method-option])}
         (name method-option)])]
     
     ;; Complexity filter
     [dual-range-slider complexity-filter 0 1 
      #(rf/dispatch [:adjust-complexity-filter %])
      "Complexity Range"]
     
     ;; Similarity threshold 
     [smooth-range-slider similarity-threshold 0 1
      #(rf/dispatch [:adjust-similarity-threshold %])
      "Similarity Threshold"]
     
     ;; Active clusters
     [:div.active-clusters
      [:h4 "Active Clusters"]
      (let [current-clusters (get clusters method {})]
        (for [[cluster-id docs] current-clusters]
          ^{:key cluster-id}
          [:div.cluster-item
           {:class (when (contains? selected cluster-id) "selected")
            :on-click #(rf/dispatch [:toggle-cluster-filter cluster-id])}
           [:div.cluster-name (name cluster-id)]
           [:div.cluster-count (str (count docs) " docs")]
           [:div.cluster-bar
            [:div.cluster-fill
             {:style {:width (str (* 100 (/ (count docs) 10)) "%")
                      :background-color (get {:technology "#667eea"
                                             :philosophy "#764ba2"  
                                             :complexity "#f68084"
                                             :humanity "#f093fb"
                                             :general "#4ecdc4"} 
                                            cluster-id "#888")}}]]]))]]))

(defn document-card [doc]
  "Smooth animated document card with rich metadata"
  [:div.document-card
   {:class (str "tone-" (name (:tone doc)) 
               " complexity-" (cond 
                               (< (:complexity doc) 0.3) "low"
                               (< (:complexity doc) 0.7) "medium"
                               :else "high"))
    :on-click #(rf/dispatch [:select-document doc])}
   
   [:div.document-header
    [:div.document-title (:name doc)]
    [:div.document-metadata
     [:span.complexity-indicator
      {:title (str "Complexity: " (.toFixed (:complexity doc) 2))}
      (repeat (inc (int (* 3 (:complexity doc)))) "●")]
     [:span.tone-badge {:class (str "tone-" (name (:tone doc)))} 
      (name (:tone doc))]]]
   
   [:div.document-preview
    (str (subs (or (:content doc) (:path doc)) 0 150) "...")]
   
   [:div.concept-tags
    (take 4 (:concepts doc))]
   
   [:div.document-stats
    [:span.word-count (str (:word-count doc 0) " words")]
    [:span.structure-type (name (:structure doc))]]])

(defn documents-grid []
  "Responsive grid with smooth filtering animations"
  (let [documents @(rf/subscribe [:documents])
        view-mode @(rf/subscribe [:view-mode])
        loading? @(rf/subscribe [:loading?])]
    
    [:div.documents-container
     (if loading?
       [:div.loading-state "🌙 Loading documents..."]
       [:div {:class (str "documents-grid " (name view-mode))}
        (for [doc documents]
          ^{:key (:path doc)}
          [document-card doc])])]))

(defn similarity-sidebar []
  "Live similarity suggestions sidebar"
  (let [selected-doc @(rf/subscribe [:selected-document])
        suggestions @(rf/subscribe [:live-suggestions])]
    
    (when selected-doc
      [:div.similarity-sidebar
       [:h4 "🌸 Similar Documents"]
       [:div.selected-doc-info
        [:div.selected-title (:name selected-doc)]
        [:div.selected-concepts
         (for [concept (take 3 (:concepts selected-doc))]
           ^{:key concept}
           [:span.concept-tag concept])]]
       
       [:div.similarity-list
        (for [similar-doc suggestions]
          ^{:key (:path similar-doc)}
          [:div.similarity-item
           {:on-click #(rf/dispatch [:select-document similar-doc])}
           [:div.similar-title (:name similar-doc)]
           [:div.similarity-score 
            (str (.toFixed (* 100 (:similarity similar-doc)) 0) "% similar")]
           [:div.similar-concepts
            (take 2 (:concepts similar-doc))]])]])))

(defn usage-hints []
  "Interactive usage instructions"
  (let [show-hints? (r/atom true)]
    (fn []
      [:div.usage-hints
       [:div {:style {:display "flex" :justify-content "space-between" :align-items "center" :margin-bottom "0.5rem"}}
        [:div.hint-title "💡 Usage Guide"]
        [:button {:style {:background "transparent" :border "1px solid rgba(255,255,255,0.2)" :color "#ff6b9d" :border-radius "4px" :padding "0.2rem 0.5rem" :cursor "pointer"}
                  :on-click #(swap! show-hints? not)}
         (if @show-hints? "Hide" "Show")]]
       
       (when @show-hints?
         [:div
          [:div.hint-section
           [:div.hint-title "🔍 Search & Explore"]
           [:div.hint-text "Type in the search box to find concepts, ideas, or themes. Live suggestions appear as you type. Try searching for \"complexity\", \"system\", or \"thinking\"."]]
          
          [:div.hint-section
           [:div.hint-title "🧠 Clustering Methods"]
           [:div.hint-text "Switch between " [:span.kbd "semantic"] ", " [:span.kbd "temporal"] ", " [:span.kbd "structural"] ", " [:span.kbd "complexity"] ", and " [:span.kbd "hybrid"] " clustering. Each uses different randomness sources for varied exploration."]]
          
          [:div.hint-section
           [:div.hint-title "🎲 Stochastic Features"]
           [:div.hint-text "The system uses entropy-weighted selection with temporal variance, complexity-driven decisions, and controlled jitter. Every refresh reveals different clustering perspectives."]]
          
          [:div.hint-section
           [:div.hint-title "📊 Interactive Controls"]
           [:div.hint-text "Adjust complexity ranges, click cluster names to filter, select documents to see similar ones. Switch between " [:span.kbd "Grid"] " and " [:span.kbd "List"] " views for different perspectives."]]])])))

(defn main-app []
  "Main Silver Lining ClojureScript application"
  [:div.silver-app
   [:div.app-header
    [:h1.app-title "🌙 Silver Lining Laboratory"]
    [:div.app-subtitle "Sophisticated semantic exploration with multi-tier randomness"]
    [usage-hints]]
   
   [:div.app-controls
    [live-search-box]
    
    [:div.view-controls
     [:button.view-toggle 
      {:class (when (= @(rf/subscribe [:view-mode]) :grid) "active")
       :on-click #(rf/dispatch [:set-view-mode :grid])}
      "Grid"]
     [:button.view-toggle
      {:class (when (= @(rf/subscribe [:view-mode]) :list) "active") 
       :on-click #(rf/dispatch [:set-view-mode :list])}
      "List"]]]
   
   [:div.app-main
    [:div.main-content
     [documents-grid]]
    
    [:div.side-panels
     [cluster-control-panel]
     [similarity-sidebar]]]
   
   ;; Live stats footer
   [:div.app-footer
    [:div.live-stats
     [:span (str @(rf/subscribe [:filtered-document-count]) " documents")]
     [:span (str (count @(rf/subscribe [:clusters])) " clusters")]
     [:span "Live clustering active"]]]])