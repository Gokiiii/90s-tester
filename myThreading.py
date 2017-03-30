import threading
import time
exitFlag = 0
threadLock = threading.Lock()
threads = []

class myThread(threading.Thread):
    def __init__(self,threadID,name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("开始线程：" + self.name)
        threadLock.acquire()
        print_time(self.name, self.counter, 5)
        threadLock.release()

def print_time(threadName,delay,counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" %(threadName,time.ctime(time.time())))
        counter -= 1

t1 = myThread(1, "Thread-1", 1)
t2 = myThread(2, "Thread-2", 2)

t1.start()
t2.start()

threads.append(t1)
threads.append(t2)

for t in threads:
    t.join()
print("退出主线程")