import threading
import time

def func1(x, y):
    for i in range(x, y):
        print(i)
#    time.sleep(10)
t1 = threading.Thread(target=func1, args=(15, 20))
t1.start()
#t1.join(5)         #注释掉这里试试
t2 = threading.Thread(target=func1, args=(5, 10))
t2.start()
#t2.join()          #注释掉这里试试

print(t1.is_alive())
print(t2.is_alive())
