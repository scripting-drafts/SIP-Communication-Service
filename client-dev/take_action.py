import time
import wikipedia
import pyjokes
import pywhatkit
import datetime
import sip_client

class take_action:
    def __init__(self, sockets_ininitiation=2):
        self.commands_list = {
            'play': self.play_on_youtube,
            'time': self.get_current_time,
            'who is': self.get_info_from_wikipedia,
            'joke': self.get_joke
        }
        
        self.sip = sip_client.sip_client()
        time.sleep(sockets_ininitiation)
        self.sip.run('receive')

    def intiate_sip_receiver(self):
        self.sip.run('receive')

    # def terminate_sip_receiver(self):
    #     # self.sip.sip_receive_thread.stop()
    #     results = self.sip.sip_receive_thread.join()

    #     return results

    def execute(self, args, timeout=2):
        data = None
        addr = None
        command = [x for x in list(self.commands_list.keys()) if x in args]
        command = args if len(command) == 0 else ''.join(command)

        if command != args:
            data = self.commands_list[command]()
            
        else:
            self.sip.sip_send(args)
            print('SIP MESSAGE SENT\n')
            print(args)

            while timeout:
                addr, data = self.sip.addr, self.sip.data
                if data is not None:
                    print(addr, data)
                    return addr, data
                time.sleep(0.2)
                timeout -= 1

            if data is None:
                raise AssertionError(f'Received empty SIP MESSAGE from {addr}\n')  
                

            # self.intiate_sip_receiver()
            # time.sleep(timeout)

            # while data == 'None':
            #     data, addr = self.sip.addr, self.sip.data

            # if data != 'None':
            #     print('SIP MESSAGE RECEIVED\n')
            
            # elif data != 'None':
            #     raise AssertionError('Received empty SIP MESSAGE\n')            

    def play_on_youtube(self):
        song = self.args.replace('play', '')
        pywhatkit.playonyt(song)

    def get_current_time(self):
        time = datetime.datetime.now().strftime('%I:%M %p')

        return time

    def get_info_from_wikipedia(self):
        person = self.args.replace('who is', '')
        try:
            info = wikipedia.summary(person, 1)
        except Exception:
            info = 'I couldn\'t understand the name'
        return info

    def get_joke(self):
        return pyjokes.get_joke()

    