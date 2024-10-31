
from threading import Thread

class TextoTerminal():
    def __init__(self):
        self.user_input = ''
        self.input_thread = Thread(target=self.input_thread)
        self.input_thread.daemon = True
        self.input_thread.start()


    def input_thread(self):
        while True:
            user_input_aux = input()
            if user_input_aux:
                self.user_input = user_input_aux
            else:
                self.user_input = None


