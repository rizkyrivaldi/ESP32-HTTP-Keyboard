from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from win32keyboard import Keyboard
import time
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.keyboard = Keyboard()

        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path # Web path /example
        query = parse_qs(urlparse(self.path).query) # Web query in dictionary
        print(query)
        if path == '/media':
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

            self.wfile.write(b'Keystroke pressed: ' + str.encode(query["press"][0]))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

if __name__ == "__main__":
    try:
        print("Program runs")
        httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
        
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        while(True):
            time.sleep(1)
            
    except KeyboardInterrupt:
        print('KeyboardInterrupt, shutting down.')
