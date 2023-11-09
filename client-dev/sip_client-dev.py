import socket
from ThreadS import ThreadS
import time

class sip_client:
    def __init__(self):
        SERVER_LOCAL_IP = None

        sip_client_port = 5061
        sip_client_ip = self.get_client_address()
        
        self.sip_server_port = 5060
        self.sip_server_ip = SERVER_LOCAL_IP

        self.threads = []
        self.sip_types = {
            'open_socket': self.open_sip_socket,
            'receive': self.sip_receive,
            'send': self.sip_send
        }
        self.queue = []

        sip_server_name = 'sip_server'
        sip_server_domain = 'sip_server.com'
        sip_server_uri = 'sip:' + sip_server_name + '@' + sip_server_domain
        sip_server_uri = sip_server_uri.lower()
        sip_server_uri = sip_server_uri.replace(' ', '')
        self.addr = ''
        self.data = None

        self.open_sip_socket(sip_client_ip, sip_client_port)

    def get_client_address(self):
        return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

    def open_sip_socket(self, sip_client_ip, sip_client_port):
        # Inbound socket
        self.sip_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sip_client_socket.bind((sip_client_ip, sip_client_port))

        self.sip_outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    def sip_receive(self):
        while True:
            data, addr = self.sip_client_socket.recvfrom(1024)
            print(addr, data)
            time.sleep(.2)


    def sip_send(self, message):
        self.sip_outbound_socket.sendto(message.encode('utf-8'), (self.sip_server_ip, self.sip_server_port))


    # def sip_send(self, message=None):
    #     if message is not None:
    #         message = message.encode(encoding='UTF-8') if type(message) is str() else message
    #         self.sip_outbound_socket.sendto(message, (self.sip_server_ip, self.sip_server_port))
    #         # self.message = None
    #         time.sleep(.1)
        
        # self.sip_client_socket.sendto(str(message.encode(encoding='UTF-8')), (self.sip_server_ip, self.sip_server_port))

    def run(self, action, args=None):
        '''
        Action Types: SEND or RECEIVE
        '''
        if args:
            sip_send_thread = ThreadS(target=self.sip_types[action], args=(args,))
            sip_send_thread.start()
            sip_send_thread.join()
        else:
            sip_receive_thread = ThreadS(target=self.sip_types[action], args=())
            sip_receive_thread.start()

    # def join(self):
    #     for thread in self.threads:
    #         thread.join()