#!/usr/bin/env python3
"""
Simple HTTP server script to serve AeroTrace simulation console locally.
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(DIRECTORY, "simulation"), **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"==================================================")
        print(f"  AeroTrace Diagnostic Console running at:")
        print(f"  http://localhost:{PORT}")
        print(f"==================================================")
        webbrowser.open(f"http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
