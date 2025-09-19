"""
Web server utility for serving HTML/CSS/JS files
"""

import http.server
import socketserver
import webbrowser
import threading
import os
from pathlib import Path


class WebServer:
    def __init__(self, port=8000, directory=None):
        self.port = port
        self.directory = directory or os.path.join(os.path.dirname(__file__), '..', '..', 'static')
        self.server = None
        self.thread = None
        
    def start(self, open_browser=True):
        """Start the web server"""
        try:
            os.chdir(self.directory)
            
            handler = http.server.SimpleHTTPRequestHandler
            
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                self.server = httpd
                print(f"Web server running at http://localhost:{self.port}")
                
                if open_browser:
                    webbrowser.open(f'http://localhost:{self.port}')
                
                httpd.serve_forever()
                
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"Port {self.port} is already in use. Trying port {self.port + 1}")
                self.port += 1
                self.start(open_browser)
            else:
                print(f"Error starting web server: {e}")
    
    def start_background(self, open_browser=True):
        """Start the web server in a background thread"""
        self.thread = threading.Thread(target=self.start, args=(open_browser,))
        self.thread.daemon = True
        self.thread.start()
        return self.thread
    
    def stop(self):
        """Stop the web server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Web server stopped")


def serve_static_files(port=8000, open_browser=True):
    """Convenience function to serve static files"""
    server = WebServer(port)
    return server.start_background(open_browser)


if __name__ == "__main__":
    # Run the web server
    server = WebServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down web server...")
        server.stop()
