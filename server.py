import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

HOST_NAME = 'localhost'
PORT_NUMBER = 9000
if 'PORT' in os.environ.keys():
    PORT_NUMBER = os.environ['PORT']

import pickle5 as pickle
 
# load the model from disk
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

class MyHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/water': {'status': 200},
            '/air': {'status': 200},
        }

        from pathlib import Path
        
        url_path = urlparse(self.path).path
        
        print(url_path)
        
        my_file = Path("."+url_path)
        
        if url_path in paths:
            self.respond({'status': 200})
        elif my_file.is_file():
            self.respond({'status': 200})
        else:            
            root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'http')
            print(root, os.path.abspath(__file__))
            if self.path == '/':
                filename = root + '/index.html'
            else:
                filename = root + self.path

            if not os.path.exists(filename):
                self.respond({'status': 404})
                return
    
            self.send_response(200)
            if filename[-4:] == '.css':
                self.send_header('Content-type', 'text/css')
            elif filename[-5:] == '.json':
                self.send_header('Content-type', 'application/javascript')
            elif filename[-3:] == '.js':
                self.send_header('Content-type', 'application/javascript')
            elif filename[-4:] == '.ico':
                self.send_header('Content-type', 'image/x-icon')
            else:
                self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(filename, 'rb') as fh:
                html = fh.read()
                #html = bytes(html, 'utf8')
                self.wfile.write(html)

    def handle_http(self, status_code, path):        
        self.send_response(status_code)
        self.end_headers()
        
        if status_code == 404:
            return bytes("404 Page Not Found",'UTF-8')
        
        content = 'GET_'
        query_components = parse_qs(urlparse(self.path).query)   
        
        path = urlparse(path).path

        if path == '/water':
            #water?temp=2&do=3&ph=7&bod=3&nit=4&cf=5
            temp = query_components["temp"][0]
            do = query_components["do"][0] 
            ph = query_components["ph"][0] 
            bod = query_components["bod"][0] 
            nit = query_components["nit"][0] 
            cf = query_components["cf"][0] 
            data = [[float(temp),float(do),float(ph),float(bod),float(nit),float(cf)]]
            pred = int(model.predict(data))
            content = str(pred)
            return bytes(content, 'UTF-8')
        elif path == '/air':
            content = 'air analysis'
            return bytes(content, 'UTF-8')
        else:
            with open("."+urlparse(self.path).path, 'rb') as file: 
                return file.read()

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
	
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
