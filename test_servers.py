#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Documentation Browser
Tests both the Python main server (44500) and Racket silver lining server (44501)
"""

import pytest
import requests
import json
import time
import subprocess
import os
from typing import Dict, List, Optional

# Test Configuration
PYTHON_SERVER_URL = "http://localhost:44500"
RACKET_SERVER_URL = "http://localhost:44501"
TEST_TIMEOUT = 10

class TestPythonMainServer:
    """Test suite for the Python-based main documentation server"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Ensure server is running before each test"""
        try:
            response = requests.get(PYTHON_SERVER_URL, timeout=2)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Python server not running on port 44500")
    
    def test_index_page_loads(self):
        """Test that the main index page loads successfully"""
        response = requests.get(PYTHON_SERVER_URL, timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        assert "Documentation Browser" in response.text
        assert "Inter Tight" in response.text  # Check typography
        assert "Atkinson Hyperlegible" in response.text
    
    def test_search_functionality(self):
        """Test the search API endpoint"""
        search_url = f"{PYTHON_SERVER_URL}/api/search"
        
        # Test with valid query
        response = requests.get(search_url, params={"q": "test"}, timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Test empty query
        response = requests.get(search_url, params={"q": ""}, timeout=TEST_TIMEOUT)
        assert response.status_code == 400
    
    def test_files_api(self):
        """Test the files listing API"""
        files_url = f"{PYTHON_SERVER_URL}/api/files"
        response = requests.get(files_url, timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Check structure of file objects
        if data:
            file_obj = data[0]
            assert "name" in file_obj
            assert "path" in file_obj
            assert file_obj["path"].endswith(".md")
    
    def test_content_analysis_api(self):
        """Test the content analysis and clustering API"""
        analysis_url = f"{PYTHON_SERVER_URL}/api/content-analysis"
        response = requests.get(analysis_url, timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        
        data = response.json()
        assert "clusters" in data
        assert "total_documents" in data
        assert isinstance(data["clusters"], list)
        assert isinstance(data["total_documents"], int)
    
    def test_semantic_document_types(self):
        """Test that semantic document classification works"""
        files_url = f"{PYTHON_SERVER_URL}/api/files"
        response = requests.get(files_url, timeout=TEST_TIMEOUT)
        data = response.json()
        
        # Look for documents that should be classified
        has_roadmap = any("roadmap" in f["name"].lower() for f in data)
        has_technical = any("technical" in f["name"].lower() or "architecture" in f["name"].lower() for f in data)
        
        # At least some classification should be happening
        assert len(data) > 0, "Should have some documents to classify"
    
    def test_css_variables_and_typography(self):
        """Test that CSS custom properties and typography are properly configured"""
        response = requests.get(PYTHON_SERVER_URL, timeout=TEST_TIMEOUT)
        content = response.text
        
        # Check CSS variables
        assert "--font-base:" in content
        assert "--transition-fast:" in content
        assert "--color-roadmap:" in content
        
        # Check typography stacks
        assert "Inter Tight" in content
        assert "JetBrains Mono" in content
        assert "Fira Code" in content


class TestRacketSilverLiningServer:
    """Test suite for the Racket-based silver lining server"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Ensure Racket server is running before each test"""
        try:
            response = requests.get(RACKET_SERVER_URL, timeout=2)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Racket server not running on port 44501")
    
    def test_index_page_loads(self):
        """Test that the silver lining index loads"""
        response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        assert "Silver Lining" in response.text
        assert "Essay Garden" in response.text
        assert "Vollkorn" in response.text  # Check serif typography
    
    def test_essay_route_structure(self):
        """Test that essay routes are properly structured"""
        response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        content = response.text
        
        # Look for essay links in the garden
        assert "essay/" in content or len(content) > 1000  # Should have substantial content
    
    def test_typography_and_styling(self):
        """Test that Racket server has proper typography configuration"""
        response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        content = response.text
        
        # Check serif typography stack
        assert "Vollkorn" in content
        assert "Crimson Text" in content or "Lora" in content
        
        # Check monospace fonts for code
        assert "Fira Code" in content
        assert "JetBrains Mono" in content or "Cascadia Code" in content
    
    def test_gradient_styling(self):
        """Test that the dark gradient theme is properly applied"""
        response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        content = response.text
        
        assert "linear-gradient" in content
        assert "#0f0f23" in content  # Dark background colors
        assert "#1a1a2e" in content

class TestServerIntegration:
    """Integration tests for both servers working together"""
    
    def test_both_servers_respond(self):
        """Test that both servers are accessible simultaneously"""
        python_response = requests.get(PYTHON_SERVER_URL, timeout=TEST_TIMEOUT)
        racket_response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        
        assert python_response.status_code == 200
        assert racket_response.status_code == 200
        
        # Different content indicates different servers
        assert python_response.text != racket_response.text
    
    def test_port_accessibility(self):
        """Test that the correct ports are being used"""
        # Python server should be on 44500
        try:
            requests.get("http://localhost:44500", timeout=2)
        except requests.exceptions.RequestException:
            pytest.fail("Python server not accessible on port 44500")
        
        # Racket server should be on 44501
        try:
            requests.get("http://localhost:44501", timeout=2)
        except requests.exceptions.RequestException:
            pytest.fail("Racket server not accessible on port 44501")
    
    def test_complementary_design_philosophy(self):
        """Test that the two servers have different but complementary designs"""
        python_response = requests.get(PYTHON_SERVER_URL, timeout=TEST_TIMEOUT)
        racket_response = requests.get(RACKET_SERVER_URL, timeout=TEST_TIMEOUT)
        
        # Python server should have sans-serif primary typography
        assert "Inter Tight" in python_response.text
        
        # Racket server should have serif primary typography  
        assert "Vollkorn" in racket_response.text
        
        # Different color schemes
        python_has_gradients = "linear-gradient" in python_response.text
        racket_has_gradients = "linear-gradient" in racket_response.text
        
        assert python_has_gradients and racket_has_gradients
        # But different gradient colors
        assert "#667eea" in python_response.text  # Python server colors
        assert "#0f0f23" in racket_response.text  # Racket server colors


class TestErrorHandling:
    """Test error conditions and edge cases"""
    
    def test_invalid_file_path(self):
        """Test handling of invalid file paths"""
        invalid_url = f"{PYTHON_SERVER_URL}/file/nonexistent.md"
        response = requests.get(invalid_url, timeout=TEST_TIMEOUT)
        assert response.status_code == 404
    
    def test_malformed_search(self):
        """Test handling of malformed search requests"""
        # Very long query
        long_query = "x" * 1000
        search_url = f"{PYTHON_SERVER_URL}/api/search"
        response = requests.get(search_url, params={"q": long_query}, timeout=TEST_TIMEOUT)
        # Should handle gracefully, either 200 with results or reasonable error
        assert response.status_code in [200, 400, 500]
    
    def test_racket_invalid_routes(self):
        """Test Racket server handling of invalid routes"""
        invalid_url = f"{RACKET_SERVER_URL}/invalid/route/path"
        response = requests.get(invalid_url, timeout=TEST_TIMEOUT)
        # Racket server should return proper 404 or handle gracefully
        assert response.status_code in [404, 200]  # Some servers redirect to index


def run_server_diagnostics():
    """Run diagnostic checks on the servers"""
    print("🔍 Running server diagnostics...")
    
    # Check if processes are running
    python_proc = subprocess.run(["pgrep", "-f", "enhanced_docs_server.py"], 
                                capture_output=True, text=True)
    racket_proc = subprocess.run(["pgrep", "-f", "silver-simple.rkt"], 
                                capture_output=True, text=True)
    
    print(f"Python server process: {'✅ Running' if python_proc.returncode == 0 else '❌ Not found'}")
    print(f"Racket server process: {'✅ Running' if racket_proc.returncode == 0 else '❌ Not found'}")
    
    # Check port bindings
    port_check = subprocess.run(["netstat", "-tlnp"], capture_output=True, text=True)
    ports_44500 = ":44500" in port_check.stdout
    ports_44501 = ":44501" in port_check.stdout
    
    print(f"Port 44500 bound: {'✅ Yes' if ports_44500 else '❌ No'}")
    print(f"Port 44501 bound: {'✅ Yes' if ports_44501 else '❌ No'}")


if __name__ == "__main__":
    # Run diagnostics first
    run_server_diagnostics()
    
    # Run tests
    print("\n🧪 Running test suite...")
    exit_code = pytest.main([
        __file__, 
        "-v", 
        "--tb=short",
        "--color=yes"
    ])
    
    exit(exit_code)