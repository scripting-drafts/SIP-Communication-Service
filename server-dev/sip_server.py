# Sets up a SIP server
import socket
import threading
import time
import string

class sip_server:
    def __init__(self):
        SIP_CLIENT_IP = None
        self.sip_server_ip = self.get_client_address()
        self.sip_server_port = 5060
    
        self.sip_client_port = 5061
        self.sip_client_ip = SIP_CLIENT_IP

        sip_server_name = 'sip_server'
        sip_server_domain = 'sip_server.com'
        sip_server_uri = 'sip:' + sip_server_name + '@' + sip_server_domain
        sip_server_uri = sip_server_uri.lower()
        sip_server_uri = sip_server_uri.replace(' ', '')
        self.addr = ''
        self.data = string.ascii_lowercase
        
        self.threads = []
        self.sip_types = {
            'open_socket': self.open_sip_socket,
            'send': self.sip_send,
            'receive': self.sip_receive
        }
        self.open_sip_socket()
        # self.sip_receive()

    def get_client_address(self):
        return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

    def open_sip_socket(self):
        # Inbound socket
        self.sip_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sip_server_socket.bind((self.sip_server_ip, self.sip_server_port))

        # Outbound socket
        self.sip_outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sip_receive(self):
        while True:
            data, addr = self.sip_server_socket.recvfrom(1024)
            if data != self.data:
                # print(data)
                self.addr = addr
                data = data.decode('utf-8')
                
                # print("From: ", addr)
                print("Data: ", data)
                
                self.data = data
                time.sleep(.1)

    def sip_send(self, message):
        self.sip_outbound_socket.sendto(message.encode('utf-8'), (self.sip_client_ip, self.sip_client_port))

    def run(self, action, args=None):
        if args is not None:
            sip_client_thread = threading.Thread(target=self.sip_types[action], args=(args,))
        else:
            sip_client_thread = threading.Thread(target=self.sip_types[action], args=())

        self.threads.append(sip_client_thread)
        sip_client_thread.start()

    def join(self):
        for thread in self.threads:
            thread.join()


        time.sleep(10)
