import threading
from time import sleep
from random import randint


class Producer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        global x
        while True:
            sleep(randint(1, 3))
            con.acquire()
        if len(x) == 5:
            print('Producer waiting....')
            con.wait()
        else:
            r = randint(1, 1000)
            print('Produced:', r)
            x.append(r)
            con.notify()
        con.release()


class Consumer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        global x
        sleep(randint(1, 3))
        con.acquire()
        if not x:
            print('Consumer is waiting....')
            con.wait()
        else:
            print('Consumed:', x.pop(0))
            con.notify()
        con.release()


con = threading.Condition()

x = []

p = Producer('Producer')
c = Consumer('Consumer')

c.start()
p.start()



