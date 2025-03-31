from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

# Global variable to store the current heart rate
current_hr = "0"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class HeartBeatHandler(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        global current_hr
        if self.path == "/hr":
            self._set_response(200)
            self.wfile.write(current_hr.encode('utf-8'))
        elif self.path == "/obs":
            self._set_response(200)
            self.wfile.write(open("./obs.html", "r").read().encode('utf-8'))
        elif self.path.startswith("/js/") or self.path.startswith("/css/"):
            self._set_response(200)
            self.wfile.write(open(".{}".format(self.path), "r").read().encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write("NOT FOUND".encode('utf-8'))

    def do_POST(self):
        global current_hr
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        self._set_response(200)
        self.wfile.write("OK".encode('utf-8'))
        data = post_data.decode('utf-8').split("=")
        print("Received BPM = {}".format(data[1]))
        current_hr = data[1]  # Update the global heart rate variable

def run(port, server_class=HTTPServer, handler_class=HeartBeatHandler):
    server_address = ("", port)

    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("""
###########################
#         STOPPING        #
###########################        
        """)
        pass
    httpd.server_close()

if __name__ == '__main__':
    port_arg = 6547
    if len(argv) == 2:
        port_arg = argv[1]

    print("This is your IP : {}".format(get_ip()))
    print("Port is {}".format(port_arg))
    if len(argv) == 2:
        run(port=int(port_arg))
    else:
        run(port_arg)