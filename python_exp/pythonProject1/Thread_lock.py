import threading
import time

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global x                    #声明全局变量
        lock.acquire()              #获取锁，进入临界区
        for i in range(3):
            x = x + i
        time.sleep(2)
        print(x)
        lock.release()              #释放锁，退出临界区

lock = threading.Lock()      #创建锁，这里也可以使用RLock
tl = []
for i in range(10):          #创建10个线程
    t = myThread()
    tl.append(t)
x = 0
for i in tl:                 #启动10个线程
    i.start()
