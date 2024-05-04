from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from win32keyboard import Keyboard
import os
import time
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.keyboard = Keyboard()

        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Parse the path
        raw_path = urlparse(self.path).path # Web path /example
        path = list(filter(None, raw_path.split('/')))

        # Parse the query
        query = parse_qs(urlparse(self.path).query) # Web query in dictionary

        if len(path) == 0:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            file_to_open = open('media.html').read()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif path[0] == 'media':
            # Reply to request
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Do the keystroke
            if "press" in query:
                self.keyboard.press(query["press"][0])

            if "hold" in query:
                self.keyboard.pressAndHold(query["hold"][0])

            if "release" in query:
                self.keyboard.release(query["release"][0])

        elif path[0] == 'assets':
            if path[1].endswith('.png'):
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(open(os.path.join(path[0], path[1]),'rb').read())

            elif path[1].endswith('.webmanifest'):
                self.send_response(200)
                self.send_header('Content-type', 'application/manifest+json')
                self.end_headers()
                self.wfile.write(open(os.path.join(path[0], path[1]),'rb').read())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

if __name__ == "__main__":
    try:
        print(f"Media Server Successfully Deployed, Port: {8000}")
        httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
        
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        while(True):
            time.sleep(1)

    except KeyboardInterrupt:
        print('KeyboardInterrupt, shutting down.')
