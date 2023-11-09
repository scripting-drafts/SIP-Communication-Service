# from http.server import SimpleHTTPRequestHandler
# import socketserver
import string
from Models.godel import godel
from sip_server import sip_server
import time

gd = godel()
sip = sip_server()
# sip.run('open_socket')

class Data_Handler:
    def __init__(self):
        # sip = sip_server()
        self.threads = []
        self.message = string.ascii_lowercase
        sip.run('receive')

    def run(self):
        while True:
            message = sip.data

            if message != self.message:
                reply = gd.generate(gd.instruction, ''.join(gd.knowledge), [message])
                sip.run('send', reply)
                self.message = message
                
                print(reply)
                print()

            time.sleep(.1)


if __name__ == "__main__":
    dh = Data_Handler()
    dh.run()







# class S(SimpleHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()

#     def do_GET(self):
#         print("got RESQUEST %s" % (self.path))
#         if self.path == '/':
#           self.path = 'Files/reply.txt'
#           return SimpleHTTPRequestHandler.do_GET(self)

#     def do_POST(self):
#         print("got POST")
#         post_body = self.rfile.read(int(self.headers['Content-Length']))
#         last_post = post_body.decode("utf-8")
#         gd.generate(gd.instruction, ''.join(gd.knowledge), [last_post])
        
#         print(last_post)

# def run(handler_class=S, port=8000):
#     httpd = socketserver.TCPServer(("", port), handler_class)
#     print('Starting httpd...')
#     httpd.serve_forever()