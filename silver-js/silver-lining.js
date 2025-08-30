/**
 * 🌙 Silver Lining Laboratory
 * Smooth semantic document exploration with multi-tier indexing
 */

class SilverLining {
    constructor() {
        this.state = {
            documents: [],
            filteredDocuments: [],
            loading: false,
            searchQuery: '',
            selectedClusters: new Set(),
            complexityFilter: [0, 1],
            similarityThreshold: 0.3,
            clusteringMethod: 'semantic',
            viewMode: 'grid',
            selectedDocument: null,
            clusters: {},
            semanticIndex: {},
            suggestions: []
        };
        
        this.debounceTimeout = null;
        this.init();
    }
    
    async init() {
        this.render();
        this.bindEvents();
        await this.fetchDocuments();
    }
    
    async fetchDocuments() {
        this.setState({ loading: true });
        
        try {
            const response = await fetch('http://localhost:44500/api/files');
            const documents = await response.json();
            
            const enhancedDocs = documents.map(doc => this.enhanceDocument(doc));
            const clusters = this.createClusters(enhancedDocs);
            const index = this.buildSemanticIndex(enhancedDocs);
            
            this.setState({
                documents: enhancedDocs,
                filteredDocuments: enhancedDocs,
                clusters,
                semanticIndex: index,
                loading: false
            });
            
        } catch (error) {
            console.error('Failed to fetch documents:', error);
            this.setState({ loading: false });
        }
    }
    
    enhanceDocument(doc) {
        const content = doc.content || doc.path || '';
        const concepts = this.extractConcepts(content);
        const complexity = this.calculateComplexity(content);
        const tone = this.analyzeTone(content);
        const structure = this.analyzeStructure(content);
        
        return {
            ...doc,
            concepts,
            complexity,
            tone,
            structure,
            wordCount: content.split(/\s+/).length,
            primaryCluster: this.classifyPrimaryCluster(concepts, tone),
            semanticVector: this.createSemanticVector(concepts)
        };
    }
    
    extractConcepts(text) {
        const words = text.toLowerCase()
            .split(/[^a-zA-Z0-9\-]+/)
            .filter(word => word.length > 3);
        
        const frequencies = {};
        words.forEach(word => {
            frequencies[word] = (frequencies[word] || 0) + 1;
        });
        
        return Object.entries(frequencies)
            .filter(([_, count]) => count >= 2)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([word]) => word);
    }
    
    calculateComplexity(text) {
        const sentences = text.split(/[.!?]+/).filter(s => s.trim());
        const words = text.split(/\s+/);
        const uniqueWords = new Set(words.map(w => w.toLowerCase()));
        
        const avgSentenceLength = sentences.length ? words.length / sentences.length : 0;
        const lexicalDiversity = words.length ? uniqueWords.size / words.length : 0;
        
        const abstractConcepts = ['system', 'complexity', 'understanding', 'philosophy', 'abstraction'];
        const abstractCount = words.filter(word => 
            abstractConcepts.includes(word.toLowerCase())
        ).length;
        
        return Math.min(1.0, 
            0.3 * Math.min(1.0, avgSentenceLength / 25) +
            0.4 * lexicalDiversity +
            0.3 * Math.min(1.0, abstractCount / 10)
        );
    }
    
    analyzeTone(text) {
        const words = text.toLowerCase().split(/\s+/);
        const positiveWords = ['good', 'great', 'beautiful', 'wonderful', 'amazing', 'elegant'];
        const contemplativeWords = ['think', 'consider', 'reflect', 'ponder', 'question', 'perhaps'];
        const technicalWords = ['system', 'interface', 'algorithm', 'implementation', 'architecture'];
        
        const posCount = words.filter(w => positiveWords.includes(w)).length;
        const contCount = words.filter(w => contemplativeWords.includes(w)).length;
        const techCount = words.filter(w => technicalWords.includes(w)).length;
        
        if (techCount > Math.max(posCount, contCount)) return 'technical';
        if (contCount > posCount) return 'contemplative';
        if (posCount > 0) return 'positive';
        return 'neutral';
    }
    
    analyzeStructure(text) {
        if (text.includes('##')) return 'sectioned';
        if (/\d+\.\s/.test(text)) return 'enumerated';
        if (/[-*]\s/.test(text)) return 'listed';
        if (text.split('\n\n').length > 4) return 'narrative';
        return 'simple';
    }
    
    classifyPrimaryCluster(concepts, tone) {
        const conceptSet = new Set(concepts);
        
        if (concepts.some(c => c.includes('technology'))) return 'technology';
        if (conceptSet.has('complexity') || conceptSet.has('simple')) return 'complexity';
        if (conceptSet.has('thinking') || conceptSet.has('philosophy')) return 'philosophy';
        if (conceptSet.has('human')) return 'humanity';
        if (tone === 'technical') return 'technical';
        return 'general';
    }
    
    createSemanticVector(concepts) {
        const weights = {
            'technology': 1.4, 'system': 1.3, 'complexity': 1.5,
            'simple': 1.4, 'thinking': 1.3, 'understanding': 1.4,
            'question': 1.3, 'human': 1.2, 'interface': 1.3, 'design': 1.2
        };
        
        const vector = {};
        concepts.forEach(concept => {
            vector[concept] = weights[concept] || 1.0;
        });
        return vector;
    }
    
    createClusters(documents) {
        return {
            semantic: this.semanticClustering(documents),
            temporal: this.temporalClustering(documents),
            structural: this.structuralClustering(documents),
            complexity: this.complexityClustering(documents),
            hybrid: this.hybridClustering(documents)
        };
    }
    
    semanticClustering(documents) {
        const clusters = {};
        documents.forEach(doc => {
            const cluster = doc.primaryCluster;
            if (!clusters[cluster]) clusters[cluster] = [];
            clusters[cluster].push(doc);
        });
        return clusters;
    }
    
    temporalClustering(documents) {
        const now = Date.now();
        const dayMs = 24 * 60 * 60 * 1000;
        
        const clusters = { recent: [], thisMonth: [], thisQuarter: [], older: [] };
        
        documents.forEach(doc => {
            const simulatedTime = now - (doc.path.length * dayMs); // Simulate based on path hash
            const ageInDays = (now - simulatedTime) / dayMs;
            
            if (ageInDays < 7) clusters.recent.push(doc);
            else if (ageInDays < 30) clusters.thisMonth.push(doc);
            else if (ageInDays < 90) clusters.thisQuarter.push(doc);
            else clusters.older.push(doc);
        });
        
        return clusters;
    }
    
    structuralClustering(documents) {
        const clusters = {};
        documents.forEach(doc => {
            const structure = doc.structure;
            if (!clusters[structure]) clusters[structure] = [];
            clusters[structure].push(doc);
        });
        return clusters;
    }
    
    complexityClustering(documents) {
        const clusters = { simple: [], moderate: [], complex: [] };
        
        documents.forEach(doc => {
            if (doc.complexity < 0.3) clusters.simple.push(doc);
            else if (doc.complexity < 0.6) clusters.moderate.push(doc);
            else clusters.complex.push(doc);
        });
        
        return clusters;
    }
    
    hybridClustering(documents) {
        const primary = this.semanticClustering(documents);
        const hybrid = {};
        
        Object.entries(primary).forEach(([cluster, docs]) => {
            if (docs.length <= 3) {
                hybrid[cluster] = docs;
            } else {
                const subClusters = this.complexityClustering(docs);
                Object.entries(subClusters).forEach(([subCluster, subDocs]) => {
                    if (subDocs.length > 0) {
                        hybrid[`${cluster}-${subCluster}`] = subDocs;
                    }
                });
            }
        });
        
        return hybrid;
    }
    
    buildSemanticIndex(documents) {
        const conceptIndex = {};
        const toneIndex = {};
        
        documents.forEach(doc => {
            doc.concepts.forEach(concept => {
                if (!conceptIndex[concept]) conceptIndex[concept] = [];
                conceptIndex[concept].push(doc);
            });
            
            if (!toneIndex[doc.tone]) toneIndex[doc.tone] = [];
            toneIndex[doc.tone].push(doc);
        });
        
        return { concepts: conceptIndex, tones: toneIndex };
    }
    
    cosineSimilarity(vec1, vec2) {
        const allKeys = new Set([...Object.keys(vec1), ...Object.keys(vec2)]);
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        
        allKeys.forEach(key => {
            const val1 = vec1[key] || 0;
            const val2 = vec2[key] || 0;
            dotProduct += val1 * val2;
            norm1 += val1 * val1;
            norm2 += val2 * val2;
        });
        
        const denominator = Math.sqrt(norm1) * Math.sqrt(norm2);
        return denominator ? dotProduct / denominator : 0;
    }
    
    findSimilarDocuments(targetDoc, threshold = 0.3) {
        const { documents } = this.state;
        
        return documents
            .filter(doc => doc.path !== targetDoc.path)
            .map(doc => ({
                ...doc,
                similarity: this.cosineSimilarity(targetDoc.semanticVector, doc.semanticVector)
            }))
            .filter(doc => doc.similarity > threshold)
            .sort((a, b) => b.similarity - a.similarity)
            .slice(0, 5);
    }
    
    filterDocuments() {
        const { documents, searchQuery, selectedClusters, complexityFilter, clusteringMethod } = this.state;
        const [minComplexity, maxComplexity] = complexityFilter;
        
        let filtered = documents;
        
        // Text search filter
        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(doc => {
                const searchableText = `${doc.name || doc.path} ${doc.concepts.join(' ')}`.toLowerCase();
                return searchableText.includes(query);
            });
        }
        
        // Cluster filter
        if (selectedClusters.size > 0) {
            filtered = filtered.filter(doc => selectedClusters.has(doc.primaryCluster));
        }
        
        // Complexity filter
        filtered = filtered.filter(doc => 
            doc.complexity >= minComplexity && doc.complexity <= maxComplexity
        );
        
        this.setState({ filteredDocuments: filtered });
    }
    
    updateSearchQuery(query) {
        this.setState({ searchQuery: query });
        
        // Generate suggestions
        if (query.length >= 2) {
            const suggestions = [...new Set(
                this.state.documents
                    .flatMap(doc => doc.concepts)
                    .filter(concept => concept.toLowerCase().includes(query.toLowerCase()))
                    .slice(0, 8)
            )];
            this.setState({ suggestions });
        } else {
            this.setState({ suggestions: [] });
        }
        
        // Debounced filtering
        clearTimeout(this.debounceTimeout);
        this.debounceTimeout = setTimeout(() => this.filterDocuments(), 150);
    }
    
    selectDocument(doc) {
        const similar = this.findSimilarDocuments(doc, this.state.similarityThreshold);
        this.setState({ 
            selectedDocument: doc,
            similarDocuments: similar
        });
    }
    
    toggleClusterFilter(clusterId) {
        const newSelected = new Set(this.state.selectedClusters);
        if (newSelected.has(clusterId)) {
            newSelected.delete(clusterId);
        } else {
            newSelected.add(clusterId);
        }
        
        this.setState({ selectedClusters: newSelected });
        setTimeout(() => this.filterDocuments(), 50);
    }
    
    setState(updates) {
        Object.assign(this.state, updates);
        this.render();
    }
    
    render() {
        const app = document.getElementById('app');
        const { loading, filteredDocuments, clusters, clusteringMethod, viewMode, selectedDocument, similarDocuments = [] } = this.state;
        
        if (loading) {
            app.innerHTML = '<div class="loading-state">🌙 Loading semantic analysis...</div>';
            return;
        }
        
        const currentClusters = clusters[clusteringMethod] || {};
        
        app.innerHTML = `
            <div class="silver-app">
                <div class="app-header">
                    <h1 class="app-title">🌙 Silver Lining Laboratory</h1>
                    <div class="app-subtitle">Smooth semantic exploration with live clustering</div>
                </div>
                
                <div class="app-controls">
                    <div class="live-search-container">
                        <input type="text" class="search-input" placeholder="Search concepts, ideas, themes..." value="${this.state.searchQuery}">
                        <div class="search-suggestions" id="suggestions"></div>
                    </div>
                    
                    <div class="view-controls">
                        <button class="view-toggle ${viewMode === 'grid' ? 'active' : ''}" data-view="grid">Grid</button>
                        <button class="view-toggle ${viewMode === 'list' ? 'active' : ''}" data-view="list">List</button>
                    </div>
                </div>
                
                <div class="app-main">
                    <div class="main-content">
                        <div class="documents-grid ${viewMode}">
                            ${filteredDocuments.map(doc => this.renderDocumentCard(doc)).join('')}
                        </div>
                    </div>
                    
                    <div class="side-panels">
                        <div class="cluster-panel">
                            <h3 class="panel-title">🧠 Live Clustering</h3>
                            
                            <div class="clustering-methods">
                                ${['semantic', 'temporal', 'structural', 'complexity', 'hybrid'].map(method => `
                                    <button class="method-button ${clusteringMethod === method ? 'active' : ''}" data-method="${method}">${method}</button>
                                `).join('')}
                            </div>
                            
                            <div class="range-control">
                                <label class="range-label">Complexity Range</label>
                                <input type="range" class="smooth-slider" id="complexity-min" min="0" max="1" step="0.01" value="${this.state.complexityFilter[0]}">
                                <input type="range" class="smooth-slider" id="complexity-max" min="0" max="1" step="0.01" value="${this.state.complexityFilter[1]}">
                            </div>
                            
                            <div class="active-clusters">
                                <h4>Active Clusters</h4>
                                ${Object.entries(currentClusters).map(([clusterId, docs]) => `
                                    <div class="cluster-item ${this.state.selectedClusters.has(clusterId) ? 'selected' : ''}" data-cluster="${clusterId}">
                                        <div class="cluster-name">${clusterId}</div>
                                        <div class="cluster-count">${docs.length} docs</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        
                        ${selectedDocument ? `
                            <div class="similarity-panel">
                                <h4 class="panel-title">🌸 Similar Documents</h4>
                                <div class="selected-doc-info">
                                    <div class="selected-title">${selectedDocument.name || selectedDocument.path}</div>
                                </div>
                                
                                ${similarDocuments.map(doc => `
                                    <div class="similarity-item" data-path="${doc.path}">
                                        <div class="similar-title">${doc.name || doc.path}</div>
                                        <div class="similarity-score">${Math.round(doc.similarity * 100)}% similar</div>
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                </div>
                
                <div class="app-footer">
                    <div class="live-stats">
                        <span>${filteredDocuments.length} documents</span>
                        <span>${Object.keys(currentClusters).length} clusters</span>
                        <span>Live clustering active</span>
                    </div>
                </div>
            </div>
        `;
        
        this.renderSuggestions();
    }
    
    renderDocumentCard(doc) {
        const complexityLevel = doc.complexity < 0.3 ? 'low' : doc.complexity < 0.7 ? 'medium' : 'high';
        const preview = (doc.content || doc.path).substring(0, 150);
        
        return `
            <div class="document-card tone-${doc.tone} complexity-${complexityLevel}" data-path="${doc.path}">
                <div class="document-title">${doc.name || doc.path}</div>
                <div class="document-preview">${preview}...</div>
                <div class="concept-tags">
                    ${doc.concepts.slice(0, 4).map(concept => `
                        <span class="concept-tag">${concept}</span>
                    `).join('')}
                </div>
                <div class="document-stats">
                    <span class="word-count">${doc.wordCount} words</span>
                    <span class="structure-type">${doc.structure}</span>
                </div>
            </div>
        `;
    }
    
    renderSuggestions() {
        const suggestionsEl = document.getElementById('suggestions');
        if (!suggestionsEl) return;
        
        if (this.state.suggestions.length > 0) {
            suggestionsEl.style.display = 'block';
            suggestionsEl.innerHTML = this.state.suggestions.map(suggestion => `
                <div class="suggestion-item" data-suggestion="${suggestion}">${suggestion}</div>
            `).join('');
        } else {
            suggestionsEl.style.display = 'none';
        }
    }
    
    bindEvents() {
        document.addEventListener('click', (e) => {
            // Search input and suggestions
            if (e.target.classList.contains('search-input')) return;
            if (e.target.classList.contains('suggestion-item')) {
                this.updateSearchQuery(e.target.dataset.suggestion);
                return;
            }
            
            // Document cards
            if (e.target.closest('.document-card')) {
                const card = e.target.closest('.document-card');
                const doc = this.state.filteredDocuments.find(d => d.path === card.dataset.path);
                if (doc) this.selectDocument(doc);
                return;
            }
            
            // View toggles
            if (e.target.classList.contains('view-toggle')) {
                this.setState({ viewMode: e.target.dataset.view });
                return;
            }
            
            // Method buttons
            if (e.target.classList.contains('method-button')) {
                this.setState({ clusteringMethod: e.target.dataset.method });
                return;
            }
            
            // Cluster filters
            if (e.target.closest('.cluster-item')) {
                const clusterId = e.target.closest('.cluster-item').dataset.cluster;
                this.toggleClusterFilter(clusterId);
                return;
            }
            
            // Similar documents
            if (e.target.closest('.similarity-item')) {
                const path = e.target.closest('.similarity-item').dataset.path;
                const doc = this.state.documents.find(d => d.path === path);
                if (doc) this.selectDocument(doc);
                return;
            }
        });
        
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('search-input')) {
                this.updateSearchQuery(e.target.value);
                return;
            }
            
            if (e.target.id === 'complexity-min' || e.target.id === 'complexity-max') {
                const minEl = document.getElementById('complexity-min');
                const maxEl = document.getElementById('complexity-max');
                if (minEl && maxEl) {
                    this.setState({ 
                        complexityFilter: [parseFloat(minEl.value), parseFloat(maxEl.value)]
                    });
                    setTimeout(() => this.filterDocuments(), 50);
                }
                return;
            }
        });
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new SilverLining());
} else {
    new SilverLining();
}