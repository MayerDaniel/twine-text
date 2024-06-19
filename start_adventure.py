import imessage
import threading
import sys
import time
import os
import adventure

class Listener:
    def __init__(self):
        self.Adv = adventure.Adventure(sys.argv[1])

    def listen(self):
        print ("The adventure is listening!")
        homedir = os.environ['HOME']
        path = homedir + "/Library/Messages/"
        
        # CHANGE THIS TO THE PHONE NUMBER OF YOUR CHOICE
        # FOR WHATEVER REASON APPLESCRIPT LIKES IT WITHOUT
        # THE AREA CODE, SO JUST PUT THE 7 DIGIT NUMBER

        # YOU CAN ADD MORE THAN ONE, JUST ADD ANOTHER LINE
        # LIKE SO:
        # self.Adv.start_adventure('XXXXXXXXXX')
        self.Adv.start_adventure('XXXXXXXXXX')
        try:
            while True:
                time.sleep(1)
                messages = imessage.get_last_message()
                threads = []
                for message in messages:
                    t = threading.Thread(target=self.Adv.read(message))
                    threads.append(t)
                    t.start()
        except KeyboardInterrupt:
            sys.exit(0)
        

def main():
    l = Listener()
    l.listen()

if __name__ == '__main__':
    main()
