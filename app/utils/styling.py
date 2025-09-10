from time import sleep
import sys

class Style():
    def typeEffect(self, msg: str, delay=0.01):
        for i in msg:
            print(i, end='')
            sys.stdout.flush()
            sleep(delay)