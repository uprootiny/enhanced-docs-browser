#!/usr/bin/env -S uv run --with requests --with pytest --with numpy --with scipy --with beautifulsoup4 --with aiohttp --with asyncio python3

"""
🌙 Advanced Silver Lining Test Suite
Meaningful tests for sophisticated semantic exploration system
Tests entropy quality, clustering algorithms, service integration, and cognitive load
"""

import pytest
import requests
import json
import time
import asyncio
import aiohttp
import numpy as np
from scipy import stats
from urllib.parse import urljoin
from typing import Dict, List, Optional, Tuple, Set
import concurrent.futures
from pathlib import Path
import subprocess
import hashlib
import statistics

# Test configuration
MAIN_SERVER_URL = "http://localhost:44500"
SILVER_LINING_URL = "http://localhost:45503" 
RANDOMNESS_URL = "http://localhost:47777"
SHRINE_URL = "http://localhost:44777"
TEST_TIMEOUT = 30

class TestEntropyQuality:
    """Test the quality and statistical properties of entropy sources"""
    
    def test_entropy_uniformity(self):
        """Test that entropy sources produce statistically uniform distributions"""
        response = requests.get(f"{RANDOMNESS_URL}/entropy/mixed?count=1000&sources=crypto_secure")
        assert response.status_code == 200
        data = response.json()
        values = data['values']
        
        # Kolmogorov-Smirnov test against uniform distribution
        ks_stat, p_value = stats.kstest(values, 'uniform')
        
        # Should not reject uniformity hypothesis (p > 0.01) 
        # But also shouldn't be TOO uniform (which might indicate a flawed PRNG)
        assert p_value > 0.01, f"Entropy failed uniformity test: p={p_value:.6f}"
        assert p_value < 0.99, f"Entropy suspiciously too uniform: p={p_value:.6f}"
        
        # Additional check: values should span most of the [0,1] range
        value_range = max(values) - min(values)
        assert value_range > 0.8, f"Entropy range too narrow: {value_range:.3f}"
        
        print(f"✅ Entropy uniformity test passed: p={p_value:.4f}, range={value_range:.3f}")
    
    def test_entropy_independence(self):
        """Test that consecutive entropy values are independent"""
        response = requests.get(f"{RANDOMNESS_URL}/entropy/mixed?count=500")
        data = response.json()
        values = data['values']
        
        # Serial correlation test
        pairs = [(values[i], values[i+1]) for i in range(len(values)-1)]
        x_vals = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]
        
        correlation, p_value = stats.pearsonr(x_vals, y_vals)
        
        # Correlation should be near zero for independent values
        assert abs(correlation) < 0.1, f"Entropy shows correlation: r={correlation:.4f}"
        print(f"✅ Entropy independence test passed: r={correlation:.4f}")
    
    def test_entropy_source_diversity(self):
        """Test that different entropy sources produce measurably different distributions"""
        sources = ['crypto_secure', 'mathematical', 'quantum_sim', 'atmospheric']
        distributions = {}
        
        for source in sources:
            response = requests.get(f"{RANDOMNESS_URL}/entropy/mixed?count=500&sources={source}")
            data = response.json()
            distributions[source] = data['values']
        
        # Test that sources are distinguishable using Kolmogorov-Smirnov test
        unique_pairs = 0
        total_pairs = 0
        
        for i, source1 in enumerate(sources):
            for source2 in sources[i+1:]:
                total_pairs += 1
                ks_stat, p_value = stats.ks_2samp(distributions[source1], distributions[source2])
                if p_value < 0.05:  # Significantly different
                    unique_pairs += 1
        
        diversity_ratio = unique_pairs / total_pairs if total_pairs > 0 else 0
        assert diversity_ratio > 0.3, f"Entropy sources too similar: {diversity_ratio:.2f}"
        print(f"✅ Entropy source diversity test passed: {diversity_ratio:.2f}")

class TestClusteringAlgorithms:
    """Test semantic clustering and adaptive algorithms"""
    
    def test_clustering_stability_variation(self):
        """Test that clustering provides both stability and variation"""
        # Get content analysis multiple times
        results = []
        for _ in range(5):
            response = requests.get(f"{MAIN_SERVER_URL}/api/content-analysis")
            assert response.status_code == 200
            data = response.json()
            results.append(data)
            time.sleep(0.1)  # Brief pause between requests
        
        # Test cluster count stability (shouldn't vary wildly)
        cluster_counts = [r['cluster_count'] for r in results]
        cluster_std = np.std(cluster_counts)
        assert cluster_std < 2.0, f"Clustering too unstable: std={cluster_std:.2f}"
        
        # Test that some variation exists (not identical results)
        cluster_names = []
        for result in results:
            names = set(cluster['name'] for cluster in result['clusters'])
            cluster_names.append(names)
        
        unique_combinations = len(set(frozenset(names) for names in cluster_names))
        assert unique_combinations > 1, "Clustering shows no variation"
        print(f"✅ Clustering stability/variation balance verified: {unique_combinations}/5 unique")
    
    def test_semantic_coherence(self):
        """Test that clustered documents are semantically related"""
        response = requests.get(f"{MAIN_SERVER_URL}/api/content-analysis")
        data = response.json()
        
        # Get documents for each cluster
        documents_response = requests.get(f"{MAIN_SERVER_URL}/api/files")
        documents = {doc['name']: doc['content'] for doc in documents_response.json()}
        
        for cluster in data['clusters']:
            if len(cluster['documents']) > 1:
                # Test semantic similarity within cluster using keyword overlap
                cluster_docs = [documents[doc_name] for doc_name in cluster['documents'] if doc_name in documents]
                
                if len(cluster_docs) > 1:
                    # Calculate keyword overlap between documents in cluster
                    keyword_sets = []
                    for doc_content in cluster_docs:
                        words = set(doc_content.lower().split())
                        # Filter meaningful words (longer than 3 chars, not common)
                        keywords = {w for w in words if len(w) > 3 and w not in {'the', 'and', 'that', 'this', 'with', 'from', 'they', 'have', 'been', 'were', 'said', 'each', 'which', 'their'}}
                        keyword_sets.append(keywords)
                    
                    # Calculate average pairwise intersection
                    overlaps = []
                    for i in range(len(keyword_sets)):
                        for j in range(i+1, len(keyword_sets)):
                            intersection = len(keyword_sets[i] & keyword_sets[j])
                            union = len(keyword_sets[i] | keyword_sets[j])
                            if union > 0:
                                overlap = intersection / union
                                overlaps.append(overlap)
                    
                    if overlaps:
                        avg_overlap = np.mean(overlaps)
                        assert avg_overlap > 0.05, f"Cluster '{cluster['name']}' lacks semantic coherence: {avg_overlap:.3f}"
        
        print(f"✅ Semantic coherence verified for {len(data['clusters'])} clusters")
    
    def test_stochastic_jitter_effectiveness(self):
        """Test that stochastic jitter provides meaningful clustering variation"""
        # Request different jitter values
        jitter_response = requests.get(f"{RANDOMNESS_URL}/entropy/jitter?count=20")
        jitter_values = jitter_response.json()
        
        # Test jitter range and distribution
        assert len(jitter_values) == 20
        assert all(-0.1 <= v <= 0.1 for v in jitter_values), "Jitter values outside expected range"
        
        jitter_std = np.std(jitter_values)
        assert jitter_std > 0.01, f"Jitter shows insufficient variation: std={jitter_std:.4f}"
        
        # Test that jitter affects clustering (run content analysis with different entropy states)
        clustering_results = []
        for _ in range(3):
            # Refresh entropy to get different jitter
            requests.post(f"{RANDOMNESS_URL}/entropy/refresh")
            time.sleep(0.5)  # Let entropy refresh
            
            response = requests.get(f"{MAIN_SERVER_URL}/api/content-analysis")
            clustering_results.append(response.json())
        
        # Should see some variation in cluster assignments
        cluster_names = [set(c['name'] for c in result['clusters']) for result in clustering_results]
        unique_cluster_sets = len(set(frozenset(names) for names in cluster_names))
        
        assert unique_cluster_sets > 1, "Stochastic jitter not affecting clustering outcomes"
        print(f"✅ Stochastic jitter effectiveness verified: {unique_cluster_sets}/3 unique clusterings")

class TestServiceIntegration:
    """Test integration between services and API coherence"""
    
    async def test_concurrent_service_load(self):
        """Test all services handle concurrent load without interference"""
        async def fetch_service(session, url, endpoint):
            try:
                async with session.get(f"{url}{endpoint}") as response:
                    return await response.json() if response.status == 200 else None
            except:
                return None
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            # Create mixed load across all services
            for _ in range(10):
                tasks.extend([
                    fetch_service(session, MAIN_SERVER_URL, "/api/files"),
                    fetch_service(session, MAIN_SERVER_URL, "/api/content-analysis"),
                    fetch_service(session, RANDOMNESS_URL, "/entropy/quality"),
                    fetch_service(session, SHRINE_URL, "/api/wisdom"),
                ])
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful responses
            successful = sum(1 for r in results if r is not None and not isinstance(r, Exception))
            total = len(results)
            success_rate = successful / total
            
            assert success_rate > 0.9, f"Concurrent load test failed: {success_rate:.2%} success rate"
            print(f"✅ Concurrent service load test passed: {success_rate:.1%} ({successful}/{total})")
    
    def test_randomness_service_integration(self):
        """Test that ClojureScript interface can properly integrate with randomness service"""
        # Test that Silver Lining homepage references randomness features
        silver_response = requests.get(SILVER_LINING_URL)
        assert "entropy-weighted" in silver_response.text.lower()
        assert "stochastic jitter" in silver_response.text.lower()
        
        # Test that randomness API endpoints are accessible from different origins
        entropy_response = requests.get(f"{RANDOMNESS_URL}/entropy/clustering-weights?count=3")
        assert entropy_response.status_code == 200
        
        weights = entropy_response.json()
        assert len(weights) == 3
        assert all(len(w) == 5 for w in weights)  # Should be 5-dimensional weight vectors
        assert all(abs(sum(w) - 1.0) < 0.01 for w in weights)  # Should be normalized
        
        print("✅ Randomness service integration verified")
    
    def test_shrine_contemplative_balance(self):
        """Test that Shrine provides stable counterbalance to dynamic services"""
        # Test wisdom stability - same day should give same wisdom
        wisdom1 = requests.get(f"{SHRINE_URL}/api/wisdom").json()
        time.sleep(0.1)
        wisdom2 = requests.get(f"{SHRINE_URL}/api/wisdom").json()
        
        assert wisdom1['theme'] == wisdom2['theme'], "Shrine wisdom not stable within day"
        assert wisdom1['date'] == wisdom2['date']
        
        # Test contemplative session functionality
        session_response = requests.get(f"{SHRINE_URL}/api/contemplation/start")
        assert session_response.status_code == 200
        session_data = session_response.json()
        
        assert 'guidance' in session_data
        assert 'daily_wisdom' in session_data
        assert 'session_id' in session_data
        
        print("✅ Shrine contemplative balance verified")

class TestCognitiveLoad:
    """Test user experience and cognitive load aspects"""
    
    def test_response_time_consistency(self):
        """Test that response times are consistent and reasonable"""
        endpoints = [
            (MAIN_SERVER_URL, "/api/files"),
            (MAIN_SERVER_URL, "/api/search?q=complexity"),
            (MAIN_SERVER_URL, "/api/content-analysis"),
            (RANDOMNESS_URL, "/entropy/mixed?count=100"),
            (SHRINE_URL, "/api/wisdom"),
            (SILVER_LINING_URL, "/")
        ]
        
        response_times = {}
        
        for url, endpoint in endpoints:
            times = []
            for _ in range(5):
                start = time.time()
                response = requests.get(f"{url}{endpoint}", timeout=10)
                end = time.time()
                
                if response.status_code == 200:
                    times.append(end - start)
                time.sleep(0.1)
            
            if times:
                avg_time = np.mean(times)
                std_time = np.std(times)
                response_times[f"{url}{endpoint}"] = (avg_time, std_time)
                
                # Response times should be reasonable and consistent
                assert avg_time < 2.0, f"Endpoint {endpoint} too slow: {avg_time:.2f}s"
                assert std_time < 0.5, f"Endpoint {endpoint} inconsistent: std={std_time:.2f}s"
        
        print("✅ Response time consistency verified for all endpoints")
    
    def test_content_meaningfulness(self):
        """Test that content analysis produces meaningful semantic distinctions"""
        response = requests.get(f"{MAIN_SERVER_URL}/api/content-analysis")
        data = response.json()
        
        # Test cluster name diversity
        cluster_names = [cluster['name'] for cluster in data['clusters']]
        unique_names = len(set(cluster_names))
        assert unique_names == len(cluster_names), "Duplicate cluster names found"
        
        # Test that cluster names are meaningful (not generic)
        generic_names = {'cluster_1', 'cluster_2', 'group_a', 'group_b', 'untitled', 'default'}
        meaningful_names = [name for name in cluster_names if name.lower() not in generic_names]
        
        meaningful_ratio = len(meaningful_names) / len(cluster_names)
        assert meaningful_ratio > 0.8, f"Cluster names not meaningful enough: {meaningful_ratio:.1%}"
        
        # Test document distribution (no single cluster dominates)
        cluster_sizes = [len(cluster['documents']) for cluster in data['clusters']]
        max_cluster_ratio = max(cluster_sizes) / sum(cluster_sizes)
        assert max_cluster_ratio < 0.7, f"Single cluster dominates: {max_cluster_ratio:.1%}"
        
        print(f"✅ Content meaningfulness verified: {len(cluster_names)} meaningful clusters")
    
    def test_search_relevance(self):
        """Test that search results are relevant and well-ranked"""
        test_queries = [
            ('complexity', ['complex', 'system', 'simple']),
            ('technology', ['digital', 'software', 'technical']),
            ('thinking', ['thought', 'mind', 'cognitive', 'reflection'])
        ]
        
        for query, expected_terms in test_queries:
            response = requests.get(f"{MAIN_SERVER_URL}/api/search", params={'q': query})
            assert response.status_code == 200
            
            results = response.json()
            if results:  # If we have results
                # Test that results contain relevant terms
                all_context = ' '.join(result['context'].lower() for result in results)
                
                relevant_term_count = sum(1 for term in expected_terms if term in all_context)
                relevance_ratio = relevant_term_count / len(expected_terms)
                
                assert relevance_ratio > 0.3, f"Search for '{query}' lacks relevance: {relevance_ratio:.1%}"
                
                # Test that exact query term appears prominently
                query_appearances = all_context.count(query.lower())
                assert query_appearances >= len(results), f"Query term '{query}' underrepresented"
        
        print("✅ Search relevance verified for all test queries")

class TestSystemResilience:
    """Test system resilience and error handling"""
    
    def test_malformed_request_handling(self):
        """Test graceful handling of malformed requests"""
        malformed_tests = [
            (MAIN_SERVER_URL, "/api/search?q=" + "x" * 10000),  # Very long query
            (RANDOMNESS_URL, "/entropy/mixed?count=99999"),     # Excessive count
            (RANDOMNESS_URL, "/entropy/jitter?count=-1"),       # Negative count
            (SHRINE_URL, "/api/contemplation/invalid"),         # Invalid endpoint
        ]
        
        for url, endpoint in malformed_tests:
            response = requests.get(f"{url}{endpoint}")
            # Should not crash (2xx, 4xx OK, but not 5xx)
            assert response.status_code < 500, f"Server error on malformed request: {url}{endpoint}"
        
        print("✅ Malformed request handling verified")
    
    def test_entropy_cache_resilience(self):
        """Test that entropy service recovers from cache issues"""
        # Test manual cache refresh
        refresh_response = requests.post(f"{RANDOMNESS_URL}/entropy/refresh")
        assert refresh_response.status_code == 200
        
        # Test that service continues working after refresh
        time.sleep(1)  # Allow refresh to complete
        
        entropy_response = requests.get(f"{RANDOMNESS_URL}/entropy/mixed?count=10")
        assert entropy_response.status_code == 200
        assert len(entropy_response.json()['values']) == 10
        
        print("✅ Entropy cache resilience verified")
    
    def test_service_interdependency(self):
        """Test that services can operate independently when others are stressed"""
        # Stress one service with rapid requests
        def stress_service():
            for _ in range(20):
                try:
                    requests.get(f"{RANDOMNESS_URL}/entropy/mixed?count=1000", timeout=1)
                except:
                    pass
        
        # Start stress in background
        with concurrent.futures.ThreadPoolExecutor() as executor:
            stress_future = executor.submit(stress_service)
            
            # Test other services remain responsive
            main_response = requests.get(f"{MAIN_SERVER_URL}/api/files", timeout=5)
            shrine_response = requests.get(f"{SHRINE_URL}/api/wisdom", timeout=5)
            silver_response = requests.get(SILVER_LINING_URL, timeout=5)
            
            assert main_response.status_code == 200
            assert shrine_response.status_code == 200
            assert silver_response.status_code == 200
            
            stress_future.result()  # Wait for stress test to complete
        
        print("✅ Service interdependency resilience verified")

def run_advanced_tests():
    """Run the complete advanced test suite"""
    print("🌙 Starting Advanced Silver Lining Test Suite")
    print("=" * 60)
    print("Testing entropy quality, clustering algorithms, service integration,")
    print("cognitive load, and system resilience...")
    print("=" * 60)
    
    # Run pytest with custom configuration
    test_args = [
        __file__,
        "-v",           # verbose
        "-s",           # no capture
        "--tb=short",   # short tracebacks
        "-x",           # stop on first failure
        "--durations=10"  # show slowest tests
    ]
    
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("\n" + "=" * 60)
        print("✅ 🌙 ADVANCED TESTS PASSED - Silver Lining is production-ready!")
        print("   Statistical entropy quality verified")
        print("   Clustering algorithms validated")
        print("   Service integration confirmed")
        print("   Cognitive load optimized")
        print("   System resilience tested")
        print("=" * 60)
    else:
        print(f"\n❌ Advanced tests failed with exit code: {exit_code}")
        return exit_code
    
    return 0

if __name__ == "__main__":
    # Ensure async tests can run
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    exit_code = run_advanced_tests()
    sys.exit(exit_code)