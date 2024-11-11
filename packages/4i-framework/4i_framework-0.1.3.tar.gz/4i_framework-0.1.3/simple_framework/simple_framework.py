# simple_framework.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qs, urlparse

class Template:
    def __init__(self, template_dir="templates"):
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.auto_reload = True
    
    def render(self, template_name, **context):
        try:
            # Reload the template every time in development mode
            self.env.cache.clear()
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            return f"""
            <html>
                <body>
                    <h1>Template Error</h1>
                    <p>{str(e)}</p>
                    <p>Template directory: {os.path.abspath('templates')}</p>
                    <p>Available templates: {self.env.list_templates()}</p>
                </body>
            </html>
            """

class Router:
    def __init__(self):
        self.routes = {}
    
    def add_route(self, path, handler):
        print(f"Adding route: {path}")
        self.routes[path] = handler
    
    def get_handler(self, path):
        return self.routes.get(path)

class Framework:
    def __init__(self, template_dir="templates"):
        self.template = Template(template_dir)
        self.router = Router()
        self.server = None
        self.is_dev_mode = False
        # Store the original handler functions, not the wrapped versions
        self._original_handlers = {}
    
    def route(self, path):
        def decorator(handler):
            # Store the original handler function
            self._original_handlers[path] = handler
            
            def wrapper(params):
                try:
                    if self.is_dev_mode and 'app' in sys.modules:
                        import importlib
                        importlib.reload(sys.modules['app'])
                    response = handler(params)
                    return response
                except Exception as e:
                    print(f"Error in route handler: {str(e)}")
                    return str(e)
            
            self.router.add_route(path, wrapper)
            return wrapper
        return decorator
    
    def reload_server(self):
        print("\nDetected changes, reloading templates...")
        
        try:
            # Clear template cache
            self.template.env.cache.clear()
            
            # Clear current routes
            self.router.routes.clear()
            
            # Restore all original routes
            for path, original_handler in self._original_handlers.items():
                def wrapper(params):
                    try:
                        response = original_handler(params)
                        return response
                    except Exception as e:
                        print(f"Error in route handler: {str(e)}")
                        return str(e)
                
                self.router.add_route(path, wrapper)
            
            print(f"Restored routes: {list(self.router.routes.keys())}")
            
        except Exception as e:
            print(f"Error during reload: {str(e)}")
            
        print(f"Available routes after reload: {list(self.router.routes.keys())}")
    
    def serve(self, host='localhost', port=8000, dev_mode=False):
        self.is_dev_mode = dev_mode
        
        def handler_class(*args):
            return RequestHandler(self, *args)
        
        self.server = HTTPServer((host, port), handler_class)
        
        if dev_mode:
            print("Running in development mode with auto-reload")
            
            class FileChangeHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    if event.src_path.endswith('.py') or event.src_path.endswith('.html'):
                        print(f"\nFile changed: {event.src_path}")
                        self.framework.reload_server()
                
                def __init__(self, framework):
                    self.framework = framework
            
            # Start file watcher
            event_handler = FileChangeHandler(self)
            observer = Observer()
            observer.schedule(event_handler, path='.', recursive=True)
            observer.start()
            
            print(f"Server running in development mode on http://{host}:{port}")
            print("Hot-reloading enabled. Press Ctrl+C to stop.")
        else:
            print(f"Server running on http://{host}:{port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            if dev_mode:
                observer.stop()
                observer.join()
            self.server.shutdown()
            self.server.server_close()

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, framework, *args):
        self.framework = framework
        super().__init__(*args)
    
    def do_GET(self):
        try:
            url = urlparse(self.path)
            print(f"Received request for path: {url.path}")
            
            handler = self.framework.router.get_handler(url.path)
            
            if handler:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                
                query = parse_qs(url.query)
                response = handler(query)
                
                if response is None:
                    response = "Error: Handler returned None"
                
                self.wfile.write(response.encode())
            else:
                self.send_error(404, f"Path {url.path} not found. Available routes: {list(self.framework.router.routes.keys())}")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            error_message = f"""
            <html>
                <body>
                    <h1>Server Error</h1>
                    <p>{str(e)}</p>
                    <p>Path: {self.path}</p>
                    <p>Available routes: {list(self.framework.router.routes.keys())}</p>
                </body>
            </html>
            """
            self.wfile.write(error_message.encode())

def create_app(template_dir="templates"):
    return Framework(template_dir)