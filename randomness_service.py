#!/usr/bin/env -S uv run --with fastapi --with uvicorn --with numpy --with scipy --with cryptography python3

"""
🎲 Randomness Service - Multi-tier Entropy Provider
Sophisticated randomness caching and distribution system for Silver Lining ecosystem
"""

import asyncio
import json
import time
import hashlib
import secrets
import math
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
from scipy import stats
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configuration
RANDOMNESS_CACHE_SIZE = 10000
ENTROPY_POOL_SIZE = 1000
REFRESH_INTERVAL = 300  # 5 minutes
SERVICE_PORT = 47777  # High port for randomness service

class EntropyPool:
    """Multi-source entropy collection and management"""
    
    def __init__(self):
        self.sources = {
            'system_time': [],
            'crypto_secure': [],
            'atmospheric': [],
            'mathematical': [],
            'quantum_sim': [],
            'content_hash': [],
            'temporal_drift': []
        }
        self.last_refresh = 0
        self.refresh_count = 0
        
    def collect_entropy(self) -> Dict[str, List[float]]:
        """Collect entropy from multiple diverse sources"""
        now = time.time()
        
        # System time microsecond variations
        time_entropy = []
        for _ in range(100):
            t = time.time_ns() % 10000
            time_entropy.append(t / 10000.0)
            
        # Cryptographically secure random
        crypto_entropy = []
        for _ in range(100):
            crypto_entropy.append(secrets.randbits(32) / (2**32))
            
        # Atmospheric noise simulation (using system state)
        atmospheric_entropy = []
        for i in range(100):
            # Simulate atmospheric noise using multiple system properties
            noise = (hash(str(now + i * 0.001)) % 10000) / 10000.0
            atmospheric_entropy.append(noise)
            
        # Mathematical chaos (logistic map variations)
        mathematical_entropy = []
        x = 0.5
        for _ in range(100):
            r = 3.9 + 0.1 * np.sin(now * 0.1)  # Time-varying parameter
            x = r * x * (1 - x)
            mathematical_entropy.append(x)
            
        # Quantum simulation (based on probability distributions)
        quantum_entropy = []
        for _ in range(100):
            # Simulate quantum measurement collapse
            phase = np.random.uniform(0, 2*np.pi)
            amplitude = abs(np.sin(phase) + 1j * np.cos(phase))**2
            quantum_entropy.append(amplitude)
            
        # Content-based hash entropy
        content_entropy = []
        base_content = f"silver_lining_{now}_{self.refresh_count}"
        for i in range(100):
            content = f"{base_content}_{i}"
            hash_val = hashlib.sha256(content.encode()).hexdigest()
            entropy_val = int(hash_val[:8], 16) / (2**32)
            content_entropy.append(entropy_val)
            
        # Temporal drift patterns
        temporal_entropy = []
        for i in range(100):
            drift = math.sin(now * 0.01 + i * 0.1) * math.cos(now * 0.007 + i * 0.13)
            normalized = (drift + 1) / 2  # Normalize to 0-1
            temporal_entropy.append(normalized)
        
        self.sources = {
            'system_time': time_entropy,
            'crypto_secure': crypto_entropy, 
            'atmospheric': atmospheric_entropy,
            'mathematical': mathematical_entropy,
            'quantum_sim': quantum_entropy,
            'content_hash': content_entropy,
            'temporal_drift': temporal_entropy
        }
        
        self.last_refresh = now
        self.refresh_count += 1
        
        return self.sources
    
    def get_mixed_entropy(self, count: int = 100, sources: Optional[List[str]] = None) -> List[float]:
        """Get mixed entropy from multiple sources"""
        if sources is None:
            sources = list(self.sources.keys())
            
        mixed = []
        for i in range(count):
            # Combine multiple sources with weighted mixing
            weights = [0.2, 0.15, 0.15, 0.15, 0.1, 0.15, 0.1]  # Source weights
            value = 0
            
            for j, source in enumerate(sources[:len(weights)]):
                if source in self.sources and self.sources[source]:
                    idx = i % len(self.sources[source])
                    value += weights[j] * self.sources[source][idx]
            
            mixed.append(value % 1.0)  # Ensure 0-1 range
            
        return mixed
    
    def get_entropy_quality(self) -> Dict[str, float]:
        """Assess entropy quality using statistical tests"""
        quality = {}
        
        for source, values in self.sources.items():
            if not values:
                quality[source] = 0.0
                continue
                
            # Chi-square test for uniformity
            hist, _ = np.histogram(values, bins=10, range=(0, 1))
            expected = len(values) / 10
            chi2_stat = np.sum((hist - expected)**2 / expected)
            
            # Convert to quality score (0-1, higher is better)
            p_value = 1 - stats.chi2.cdf(chi2_stat, df=9)
            quality[source] = min(1.0, p_value * 2)  # Scale for display
            
        return quality

class RandomnessCache:
    """High-performance randomness caching system"""
    
    def __init__(self):
        self.entropy_pool = EntropyPool()
        self.cache = {
            'stochastic_jitter': [],
            'clustering_weights': [],
            'temporal_variance': [],
            'content_seeds': [],
            'similarity_thresholds': [],
            'exploration_paths': []
        }
        self.cache_metadata = {}
        self.last_generation = {}
        
    async def generate_cache(self):
        """Generate fresh randomness cache"""
        print("🎲 Generating fresh randomness cache...")
        
        # Collect fresh entropy
        entropy = self.entropy_pool.collect_entropy()
        mixed_entropy = self.entropy_pool.get_mixed_entropy(RANDOMNESS_CACHE_SIZE)
        
        # Generate different types of randomness for different use cases
        
        # Stochastic jitter values (-0.5 to 0.5) for clustering perturbation
        self.cache['stochastic_jitter'] = [
            (val - 0.5) * 0.2 for val in mixed_entropy[:2000]  # Small jitter values
        ]
        
        # Clustering weight vectors (normalized)
        clustering_weights = []
        for i in range(0, len(mixed_entropy)-5, 5):
            weights = mixed_entropy[i:i+5]
            weight_sum = sum(weights)
            if weight_sum > 0:
                normalized = [w/weight_sum for w in weights]
                clustering_weights.append(normalized)
        self.cache['clustering_weights'] = clustering_weights
        
        # Temporal variance multipliers (0.5 to 2.0)
        self.cache['temporal_variance'] = [
            0.5 + val * 1.5 for val in mixed_entropy[2000:4000]
        ]
        
        # Content-based seeds for hash variations
        self.cache['content_seeds'] = [
            int(val * 2**31) for val in mixed_entropy[4000:6000]
        ]
        
        # Dynamic similarity thresholds (0.1 to 0.8)
        self.cache['similarity_thresholds'] = [
            0.1 + val * 0.7 for val in mixed_entropy[6000:8000]
        ]
        
        # Exploration path randomness (for UI clustering exploration)
        self.cache['exploration_paths'] = [
            val for val in mixed_entropy[8000:]
        ]
        
        # Update metadata
        now = time.time()
        for cache_type in self.cache.keys():
            self.cache_metadata[cache_type] = {
                'generated_at': now,
                'count': len(self.cache[cache_type]),
                'quality': self.entropy_pool.get_entropy_quality(),
                'refresh_count': self.entropy_pool.refresh_count
            }
        
        print(f"✅ Cache generated with {len(mixed_entropy)} entropy values")

randomness_cache = RandomnessCache()

# FastAPI app setup
app = FastAPI(
    title="🎲 Silver Lining Randomness Service",
    description="Multi-tier entropy provider for sophisticated semantic exploration",
    version="1.0.0"
)

# CORS middleware for ClojureScript integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Service status and information"""
    return {
        "service": "🎲 Silver Lining Randomness Service",
        "status": "active",
        "entropy_sources": len(randomness_cache.entropy_pool.sources),
        "cache_types": list(randomness_cache.cache.keys()),
        "last_refresh": randomness_cache.entropy_pool.last_refresh,
        "quality_metrics": randomness_cache.entropy_pool.get_entropy_quality()
    }

@app.get("/entropy/jitter")
async def get_stochastic_jitter(
    count: int = Query(default=10, ge=1, le=1000, description="Number of jitter values")
) -> List[float]:
    """Get stochastic jitter values for clustering perturbation"""
    if not randomness_cache.cache['stochastic_jitter']:
        await randomness_cache.generate_cache()
    
    values = randomness_cache.cache['stochastic_jitter'][:count]
    return values

@app.get("/entropy/clustering-weights")
async def get_clustering_weights(
    count: int = Query(default=5, ge=1, le=100, description="Number of weight vectors")
) -> List[List[float]]:
    """Get entropy-weighted clustering weight vectors"""
    if not randomness_cache.cache['clustering_weights']:
        await randomness_cache.generate_cache()
    
    weights = randomness_cache.cache['clustering_weights'][:count]
    return weights

@app.get("/entropy/temporal-variance")
async def get_temporal_variance(
    count: int = Query(default=10, ge=1, le=1000, description="Number of variance multipliers")
) -> List[float]:
    """Get temporal variance multipliers for time-based randomness"""
    if not randomness_cache.cache['temporal_variance']:
        await randomness_cache.generate_cache()
        
    values = randomness_cache.cache['temporal_variance'][:count]
    return values

@app.get("/entropy/similarity-thresholds")
async def get_similarity_thresholds(
    count: int = Query(default=10, ge=1, le=1000, description="Number of threshold values")
) -> List[float]:
    """Get dynamic similarity thresholds for adaptive clustering"""
    if not randomness_cache.cache['similarity_thresholds']:
        await randomness_cache.generate_cache()
        
    values = randomness_cache.cache['similarity_thresholds'][:count]
    return values

@app.get("/entropy/exploration-paths")
async def get_exploration_paths(
    count: int = Query(default=50, ge=1, le=1000, description="Number of path values")
) -> List[float]:
    """Get randomness for UI exploration path generation"""
    if not randomness_cache.cache['exploration_paths']:
        await randomness_cache.generate_cache()
        
    values = randomness_cache.cache['exploration_paths'][:count]
    return values

@app.get("/entropy/mixed")
async def get_mixed_entropy(
    count: int = Query(default=100, ge=1, le=5000, description="Number of mixed entropy values"),
    sources: Optional[str] = Query(default=None, description="Comma-separated entropy sources")
) -> Dict[str, Any]:
    """Get mixed entropy from multiple sources"""
    source_list = None
    if sources:
        source_list = [s.strip() for s in sources.split(',')]
    
    values = randomness_cache.entropy_pool.get_mixed_entropy(count, source_list)
    
    return {
        "values": values,
        "count": len(values),
        "sources_used": source_list or list(randomness_cache.entropy_pool.sources.keys()),
        "quality": randomness_cache.entropy_pool.get_entropy_quality(),
        "metadata": {
            "generated_at": time.time(),
            "refresh_count": randomness_cache.entropy_pool.refresh_count
        }
    }

@app.get("/entropy/quality")
async def get_entropy_quality():
    """Get entropy quality metrics and statistics"""
    quality = randomness_cache.entropy_pool.get_entropy_quality()
    
    cache_stats = {}
    for cache_type, metadata in randomness_cache.cache_metadata.items():
        cache_stats[cache_type] = {
            "count": metadata.get("count", 0),
            "age_seconds": time.time() - metadata.get("generated_at", 0),
            "refresh_count": metadata.get("refresh_count", 0)
        }
    
    return {
        "entropy_quality": quality,
        "cache_statistics": cache_stats,
        "overall_quality": np.mean(list(quality.values())) if quality else 0,
        "entropy_sources": list(randomness_cache.entropy_pool.sources.keys())
    }

@app.post("/entropy/refresh")
async def refresh_entropy_cache(background_tasks: BackgroundTasks):
    """Manually refresh the entropy cache"""
    background_tasks.add_task(randomness_cache.generate_cache)
    
    return {
        "message": "🎲 Entropy cache refresh initiated",
        "previous_refresh": randomness_cache.entropy_pool.last_refresh,
        "refresh_count": randomness_cache.entropy_pool.refresh_count
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    cache_healthy = all(len(cache) > 0 for cache in randomness_cache.cache.values())
    entropy_fresh = (time.time() - randomness_cache.entropy_pool.last_refresh) < 600  # 10 minutes
    
    return {
        "status": "healthy" if cache_healthy and entropy_fresh else "degraded",
        "cache_populated": cache_healthy,
        "entropy_fresh": entropy_fresh,
        "service": "🎲 Randomness Service",
        "uptime_seconds": time.time()
    }

async def periodic_cache_refresh():
    """Background task to refresh cache periodically"""
    while True:
        await asyncio.sleep(REFRESH_INTERVAL)
        try:
            await randomness_cache.generate_cache()
            print(f"🔄 Automatic cache refresh completed at {datetime.now()}")
        except Exception as e:
            print(f"❌ Cache refresh failed: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize randomness cache on startup"""
    print("🎲 Starting Silver Lining Randomness Service...")
    await randomness_cache.generate_cache()
    
    # Start periodic refresh task
    asyncio.create_task(periodic_cache_refresh())
    print(f"✅ Randomness service ready on port {SERVICE_PORT}")

def main():
    """Run the randomness service"""
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=SERVICE_PORT,
        log_level="info"
    )

if __name__ == "__main__":
    main()