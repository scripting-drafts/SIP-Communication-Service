import speech_recognition as sr
import pyttsx3
from take_action import take_action
import argparse
from platform_agnostic_terminate_process import pkill

class conversational:
    def __init__(self):
        self.tc = take_action()

        parser = argparse.ArgumentParser(description ='Relay command to server and get reply')
        parser.add_argument('-i', '--input_type', metavar = 'input_type', 
                            required = True, choices = {'text', 'voice'}, 
                            action ='store',
                            default = 'voice', help ='Input type: text or voice')

        self.args = parser.parse_args()
        # print(self.args.input_type)
        
        if self.args.input_type == 'voice':
            self.listener = sr.Recognizer()
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)

        self.result = None
        self.command = None

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def take_voice_command(self):
        try:
            with sr.Microphone() as source:
                self.talk('say what you want to')
                print('listening...')
                while True:
                    try:
                        command = self.get_voice_command(source=source)
                        voice_proc = command.pid

                        if self.command != command and command != '':
                            addr, data = self.tc.execute(command)
                            print(addr, data)
                            self.talk(data)

                            self.command = command

                        pkill(voice_proc)

                    except KeyboardInterrupt:
                        break

        except Exception as e:
            print(e)
            exit()
        
        # if 'command' in locals():
        #     return command
        # else:
        #     return None

    def get_voice_command(self, source):
        voice = self.listener.listen(source, timeout=None, phrase_time_limit=30)                            
        command = self.listener.recognize_google(voice)
        command = command.lower()
        print(command)

        return command

    def take_text_command(self):
        while True:
            try:
                command = input('Enter command: ')
                if self.command != command:
                    result = self.tc.execute(command)
                    print(result)

                    self.result = result
                    self.command = command
                    
            except KeyboardInterrupt:
                break

    def run(self):
        if self.args.input_type == 'voice':
            self.take_voice_command()
        elif self.args.input_type == 'text':
            self.take_text_command()

if __name__ == '__main__':
    j = conversational()
    j.run()
    