#!/usr/bin/env -S uv run --with requests python3

"""
🌙 ClojureScript Silver Lining Server
Serves the sophisticated semantic exploration interface
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse

class SilverCORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        """Override to serve .cljs files as JavaScript"""
        if path.endswith('.cljs'):
            return 'application/javascript'
        return super().guess_type(path)

def main():
    PORT = 45503  # High port as requested
    
    # Change to the resources/public directory where our files are
    public_dir = '/home/uprootiny/enhanced-docs-browser/silver-cljs/resources/public'
    os.chdir(public_dir)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), SilverCORSHTTPRequestHandler) as httpd:
        print(f"🌙 Silver Lining ClojureScript serving at http://localhost:{PORT}")
        print(f"📁 Serving from: {os.getcwd()}")
        print("✨ Sophisticated multi-tier semantic exploration ready!")
        print("🎲 With stochastic jitter and entropy-weighted clustering")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🌙 Silver Lining server shutting down gracefully...")

if __name__ == "__main__":
    main()