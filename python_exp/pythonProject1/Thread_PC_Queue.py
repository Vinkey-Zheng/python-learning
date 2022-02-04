import threading
import time
import queue

class Producer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        
    def run(self):
        for i in range(10):
            myqueue.put(i)
            print(self.getName(), ' put ', i, ' to queue.')

class Consumer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        
    def run(self):
        for i in range(10):
            print(self.getName(), ' get ', myqueue.get(), ' from queue.')

myqueue = queue.Queue()
Producer('Producer').start()
Consumer('Consumer').start()
