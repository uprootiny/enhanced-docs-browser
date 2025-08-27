#!/usr/bin/env python3
"""
Enhanced documentation server with ripgrep search and beautiful typography.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import urllib.parse
import subprocess
import markdown
import re
from pathlib import Path
import mimetypes

class EnhancedDocsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if path == '/':
            self.serve_index()
        elif path == '/search':
            self.serve_search(query.get('q', [''])[0])
        elif path == '/api/search':
            self.serve_api_search(query.get('q', [''])[0])
        elif path == '/api/files':
            self.serve_api_files()
        elif path == '/api/content-analysis':
            self.serve_content_analysis()
        elif path.startswith('/file/'):
            file_path = urllib.parse.unquote(path[6:])  # Remove '/file/'
            self.serve_file(file_path)
        elif path.startswith('/raw/'):
            file_path = urllib.parse.unquote(path[5:])  # Remove '/raw/'
            self.serve_raw_file(file_path)
        else:
            self.send_error(404)

    def serve_index(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Browser</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700&family=Jetbrains+Mono:wght@400;500&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* Fluid Typography */
            --font-xs: clamp(0.75rem, 0.875vw, 0.875rem);
            --font-sm: clamp(0.875rem, 1vw, 1rem);
            --font-base: clamp(1rem, 1.125vw, 1.125rem);
            --font-lg: clamp(1.125rem, 1.25vw, 1.25rem);
            --font-xl: clamp(1.25rem, 1.5vw, 1.5rem);
            --font-2xl: clamp(1.5rem, 2vw, 2rem);
            --font-3xl: clamp(2rem, 2.5vw, 2.5rem);
            
            /* Animation Tokens */
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
            --easing-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
            
            /* Spacing */
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-12: 3rem;
            --space-16: 4rem;
            
            /* Semantic Colors */
            --color-roadmap: #e53e3e;
            --color-technical: #667eea;
            --color-essay: #38a169;
            --color-analysis: #d69e2e;
            --color-project: #9f7aea;
            --color-memo: #0bc5ea;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        body {
            font-family: 'Inter Tight', 'Atkinson Hyperlegible', sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-size: var(--font-base);
        }
        
        .main-layout {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: var(--space-6);
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-8);
        }
        
        .primary-content {
            min-width: 0;
        }
        
        .auxiliary-sidebar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: var(--space-6);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            position: sticky;
            top: var(--space-8);
            max-height: calc(100vh - var(--space-16));
            overflow-y: auto;
            transition: all var(--transition-base);
        }
        
        @media (max-width: 1024px) {
            .main-layout {
                grid-template-columns: 1fr;
                padding: var(--space-4);
            }
            .auxiliary-sidebar {
                order: -1;
                position: static;
                max-height: none;
            }
        }
        
        .header {
            text-align: center;
            margin-bottom: var(--space-12);
            color: white;
        }
        
        .header h1 {
            font-size: var(--font-3xl);
            font-weight: 700;
            margin-bottom: var(--space-4);
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            animation: fadeInUp 0.6s var(--easing-bounce);
        }
        
        .header p {
            font-size: var(--font-lg);
            opacity: 0.9;
            animation: fadeInUp 0.6s var(--easing-bounce) 0.2s both;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .breadcrumbs {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: var(--space-3) var(--space-4);
            margin-bottom: var(--space-6);
            color: white;
            font-size: var(--font-sm);
            transition: all var(--transition-fast);
        }
        
        .breadcrumbs:hover {
            background: rgba(255, 255, 255, 0.15);
        }
        
        .breadcrumb-item {
            display: inline-block;
            opacity: 0.7;
            transition: opacity var(--transition-fast);
        }
        
        .breadcrumb-item:hover {
            opacity: 1;
        }
        
        .breadcrumb-separator {
            margin: 0 var(--space-2);
            opacity: 0.5;
        }
        
        .pin-toggle {
            float: right;
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            padding: var(--space-1);
            border-radius: 4px;
            transition: all var(--transition-fast);
        }
        
        .pin-toggle:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }
        
        .pin-toggle.pinned {
            color: #ffd700;
            transform: rotate(15deg);
        }
        
        .search-section {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            margin-bottom: 2rem;
        }
        
        .search-box {
            position: relative;
            margin-bottom: 2rem;
        }
        
        .search-input {
            width: 100%;
            padding: var(--space-4) var(--space-6);
            font-size: var(--font-lg);
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            outline: none;
            transition: all var(--transition-base);
            background: white;
        }
        
        .search-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-1px);
        }
        
        .search-input.typing {
            border-color: #38a169;
            box-shadow: 0 0 0 3px rgba(56, 161, 105, 0.1);
        }
        
        .search-status {
            position: absolute;
            right: var(--space-4);
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            opacity: 0;
            transition: opacity var(--transition-fast);
        }
        
        .search-status.visible {
            opacity: 1;
        }
        
        .typing-indicator {
            color: #38a169;
            font-size: var(--font-sm);
        }
        
        .search-count {
            color: #718096;
            font-size: var(--font-sm);
        }
        
        .search-btn {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            padding: 0.5rem 1rem;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        
        .search-btn:hover {
            background: #5a67d8;
        }
        
        .files-section {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #2d3748;
        }
        
        .file-list {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        }
        
        .file-item {
            display: block;
            padding: var(--space-4);
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            text-decoration: none;
            color: #2d3748;
            transition: all var(--transition-base);
            position: relative;
            overflow: hidden;
        }
        
        .file-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: var(--item-color, #667eea);
            transform: translateX(-4px);
            transition: transform var(--transition-base);
        }
        
        .file-item:hover {
            background: #edf2f7;
            border-color: var(--item-color, #667eea);
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 8px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        }
        
        .file-item:hover::before {
            transform: translateX(0);
        }
        
        .file-item.pinned {
            border-color: #ffd700;
            background: linear-gradient(135deg, #fff9e6 0%, #f7fafc 100%);
        }
        
        .file-item.pinned .pin-indicator {
            position: absolute;
            top: var(--space-2);
            right: var(--space-2);
            color: #ffd700;
            font-size: var(--font-xs);
        }
        
        /* Semantic tinting */
        .file-item[data-type="roadmap"] { --item-color: var(--color-roadmap); }
        .file-item[data-type="technical"] { --item-color: var(--color-technical); }
        .file-item[data-type="essay"] { --item-color: var(--color-essay); }
        .file-item[data-type="analysis"] { --item-color: var(--color-analysis); }
        .file-item[data-type="project"] { --item-color: var(--color-project); }
        .file-item[data-type="memo"] { --item-color: var(--color-memo); }
        
        .file-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .file-path {
            font-size: 0.9rem;
            color: #718096;
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
        }
        
        .search-results {
            margin-top: 2rem;
        }
        
        .result-item {
            background: #f7fafc;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
        }
        
        .result-file {
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        
        .result-file a {
            color: #667eea;
            text-decoration: none;
        }
        
        .result-file a:hover {
            text-decoration: underline;
        }
        
        .result-context {
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.9rem;
            background: white;
            padding: 0.5rem;
            border-radius: 4px;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        
        .highlight {
            background: #fed7d7;
            padding: 2px 4px;
            border-radius: 2px;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #718096;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .file-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Documentation Browser</h1>
            <p>Search and explore hundreds of essays and technical documents</p>
        </div>
        
        <div class="search-section">
            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" placeholder="Search across all documents... (e.g., 'ClojureScript', 'TDA', 'roadmap')">
                <button class="search-btn" onclick="performSearch()">Search</button>
            </div>
            <div id="searchResults" class="search-results" style="display: none;"></div>
        </div>
        
        <div class="files-section">
            <h2 class="section-title">📄 All Documents</h2>
            <div id="filesList" class="file-list">
                <div class="loading">Loading documents...</div>
            </div>
        </div>
    </div>

    <script>
        // Load all files on page load
        document.addEventListener('DOMContentLoaded', loadFiles);
        
        // Search on Enter key
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
        
        async function loadFiles() {
            try {
                const response = await fetch('/api/files');
                const files = await response.json();
                
                const filesList = document.getElementById('filesList');
                
                if (files.length === 0) {
                    filesList.innerHTML = '<div class="loading">No documents found</div>';
                    return;
                }
                
                filesList.innerHTML = files.map(file => `
                    <a href="/file/${encodeURIComponent(file.path)}" class="file-item">
                        <div class="file-name">${file.name}</div>
                        <div class="file-path">${file.path}</div>
                    </a>
                `).join('');
            } catch (error) {
                console.error('Error loading files:', error);
                document.getElementById('filesList').innerHTML = 
                    '<div class="loading">Error loading documents</div>';
            }
        }
        
        async function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            const resultsDiv = document.getElementById('searchResults');
            
            if (!query) {
                resultsDiv.style.display = 'none';
                return;
            }
            
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div class="loading">Searching...</div>';
            
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const results = await response.json();
                
                if (results.length === 0) {
                    resultsDiv.innerHTML = '<div class="loading">No results found</div>';
                    return;
                }
                
                resultsDiv.innerHTML = `
                    <h3 class="section-title">🔍 Search Results (${results.length})</h3>
                    ${results.map(result => `
                        <div class="result-item">
                            <div class="result-file">
                                📄 <a href="/file/${encodeURIComponent(result.file)}">${result.file}</a>
                                ${result.line ? `(line ${result.line})` : ''}
                            </div>
                            ${result.context ? `<div class="result-context">${escapeHtml(result.context)}</div>` : ''}
                        </div>
                    `).join('')}
                `;
            } catch (error) {
                console.error('Error searching:', error);
                resultsDiv.innerHTML = '<div class="loading">Error performing search</div>';
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_api_files(self):
        """Get all markdown files using ripgrep for fast discovery"""
        try:
            # Use ripgrep to find all .md files, excluding noise directories
            result = subprocess.run([
                'rg', '--files', '--type', 'md', 
                '--glob', '!node_modules/**',
                '--glob', '!.git/**',
                '--glob', '!**/node_modules/**',
                '--glob', '!**/.git/**',
                '--glob', '!backup/**',
                '--glob', '!**/.npm/**',
                '--glob', '!**/.cache/**',
                '--glob', '!**/venv/**',
                '--glob', '!**/__pycache__/**',
                '/home/uprootiny'
            ], capture_output=True, text=True, timeout=10)
            
            files = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        path = line.strip()
                        name = os.path.basename(path)
                        files.append({
                            'name': name,
                            'path': path
                        })
            
            # Sort by name
            files.sort(key=lambda x: x['name'].lower())
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files, indent=2).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def serve_api_search(self, query):
        """Search using ripgrep for fast full-text search"""
        if not query:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No query provided'}).encode())
            return
        
        try:
            # Use ripgrep for fast search, excluding noise directories
            result = subprocess.run([
                'rg', '--type', 'md', '-n', '-C', '2', '-i', query,
                '--glob', '!node_modules/**',
                '--glob', '!.git/**', 
                '--glob', '!**/node_modules/**',
                '--glob', '!**/.git/**',
                '--glob', '!backup/**',
                '--glob', '!**/.npm/**',
                '--glob', '!**/.cache/**',
                '--glob', '!**/venv/**',
                '--glob', '!**/__pycache__/**',
                '/home/uprootiny'
            ], capture_output=True, text=True, timeout=10)
            
            results = []
            current_file = None
            current_context = []
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if not line:
                        continue
                    
                    # Parse ripgrep output format: filename:line:content
                    parts = line.split(':', 3)
                    if len(parts) >= 3:
                        file_path = parts[0]
                        line_num = parts[1]
                        content = ':'.join(parts[2:]) if len(parts) > 3 else parts[2]
                        
                        # Skip if it's just a separator line
                        if content.strip() == '--':
                            continue
                        
                        if current_file != file_path:
                            if current_file and current_context:
                                results.append({
                                    'file': current_file,
                                    'context': '\n'.join(current_context)
                                })
                            current_file = file_path
                            current_context = []
                        
                        if line_num.isdigit():
                            current_context.append(f"{line_num}: {content}")
                        else:
                            current_context.append(content)
                
                # Add the last result
                if current_file and current_context:
                    results.append({
                        'file': current_file,
                        'context': '\n'.join(current_context)
                    })
            
            # Limit results to prevent overwhelming
            results = results[:50]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results, indent=2).encode())
            
        except subprocess.TimeoutExpired:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Search timeout'}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def serve_content_analysis(self):
        """Provide document analysis and clustering information"""
        try:
            # Use ripgrep to get a sample of document content for analysis
            result = subprocess.run([
                'rg', '--files', '--type', 'md', 
                '--glob', '!node_modules/**',
                '--glob', '!.git/**',
                '--glob', '!**/node_modules/**',
                '--glob', '!**/.git/**',
                '--glob', '!backup/**',
                '/home/uprootiny'
            ], capture_output=True, text=True, timeout=10)
            
            files = []
            if result.returncode == 0:
                files = [line.strip() for line in result.stdout.strip().split('\n') if line]
            
            # Simple clustering by filename patterns
            clusters = {}
            for file_path in files:
                filename = os.path.basename(file_path).lower()
                
                if 'roadmap' in filename or 'plan' in filename:
                    cluster_type = 'roadmap'
                elif 'technical' in filename or 'architecture' in filename or 'api' in filename:
                    cluster_type = 'technical'
                elif 'essay' in filename or 'thought' in filename:
                    cluster_type = 'essay'
                elif 'analysis' in filename or 'report' in filename or 'assessment' in filename:
                    cluster_type = 'analysis'
                elif 'project' in filename or 'implementation' in filename:
                    cluster_type = 'project'
                elif 'memo' in filename or 'note' in filename or 'brief' in filename:
                    cluster_type = 'memo'
                else:
                    cluster_type = 'technical'
                
                if cluster_type not in clusters:
                    clusters[cluster_type] = []
                clusters[cluster_type].append({
                    'path': file_path,
                    'name': os.path.basename(file_path)
                })
            
            # Format clusters for frontend
            formatted_clusters = []
            for cluster_type, documents in clusters.items():
                formatted_clusters.append({
                    'name': cluster_type.title(),
                    'count': len(documents),
                    'type': cluster_type,
                    'documents': documents[:5]  # Limit for performance
                })
            
            analysis = {
                'clusters': formatted_clusters,
                'total_documents': len(files),
                'cluster_count': len(clusters)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(analysis, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def serve_file(self, file_path):
        """Serve a markdown file with beautiful formatting"""
        try:
            if not os.path.exists(file_path) or not file_path.endswith('.md'):
                self.send_error(404)
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=['codehilite', 'fenced_code', 'tables', 'toc'])
            html_content = md.convert(content)
            
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(file_path)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter Tight', 'Atkinson Hyperlegible', sans-serif;
            line-height: 1.7;
            color: #2d3748;
            background: #f7fafc;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .file-path {{
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        
        .nav {{
            padding: 1rem 2rem;
            border-bottom: 1px solid #e2e8f0;
            background: #f7fafc;
        }}
        
        .nav a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        
        .nav a:hover {{
            text-decoration: underline;
        }}
        
        .content {{
            padding: 3rem;
            max-width: none;
        }}
        
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #1a202c;
            line-height: 1.3;
        }}
        
        .content h1 {{ font-size: 2.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
        .content h2 {{ font-size: 2rem; }}
        .content h3 {{ font-size: 1.5rem; }}
        .content h4 {{ font-size: 1.25rem; }}
        
        .content p {{
            margin-bottom: 1.5rem;
            text-align: justify;
        }}
        
        .content ul, .content ol {{
            margin-bottom: 1.5rem;
            padding-left: 2rem;
        }}
        
        .content li {{
            margin-bottom: 0.5rem;
        }}
        
        .content code {{
            background: #edf2f7;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.9em;
        }}
        
        .content pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 1.5rem;
        }}
        
        .content pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        
        .content blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: #4a5568;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.5rem;
        }}
        
        .content th, .content td {{
            border: 1px solid #e2e8f0;
            padding: 0.75rem;
            text-align: left;
        }}
        
        .content th {{
            background: #f7fafc;
            font-weight: 600;
        }}
        
        .content a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px dotted #667eea;
        }}
        
        .content a:hover {{
            background: #edf2f7;
            text-decoration: none;
            border-bottom: 1px solid #667eea;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .content {{ padding: 2rem 1.5rem; }}
            .content h1 {{ font-size: 2rem; }}
            .content h2 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 {os.path.basename(file_path)}</h1>
            <div class="file-path">{file_path}</div>
        </div>
        
        <div class="nav">
            <a href="/">← Back to Browser</a>
            <span style="margin: 0 1rem;">|</span>
            <a href="/raw/{urllib.parse.quote(file_path)}">View Raw</a>
        </div>
        
        <div class="content">
            {html_content}
        </div>
    </div>
</body>
</html>"""
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            
        except Exception as e:
            self.send_error(500)

    def serve_raw_file(self, file_path):
        """Serve raw markdown file"""
        try:
            if not os.path.exists(file_path):
                self.send_error(404)
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode())
            
        except Exception as e:
            self.send_error(500)

def run_server(port=44500):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, EnhancedDocsHandler)
    print(f"🚀 Enhanced Documentation Server running at http://0.0.0.0:{port}")
    print(f"   Search across hundreds of essays and technical documents")
    print(f"   Beautiful typography and responsive design")
    print(f"   Powered by ripgrep for fast full-text search")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()