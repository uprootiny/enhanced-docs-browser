#!/usr/bin/env -S uv run --with requests python3

"""
🌙 Silver Lining HTTP Server
Simple server for the JavaScript-based semantic interface
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    PORT = 44504
    
    # Change to the silver-js directory
    os.chdir('/home/uprootiny/enhanced-docs-browser/silver-js')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🌙 Silver Lining serving at http://localhost:{PORT}")
        print(f"📁 Serving from: {os.getcwd()}")
        print("✨ Ready for smooth semantic exploration!")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🌙 Silver Lining server shutting down gracefully...")

if __name__ == "__main__":
    main()