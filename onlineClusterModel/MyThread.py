#coding=utf-8

import threading
import time
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        time.sleep(1)
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except:
            return None

def add(a, b):
    return a + b

if __name__ == "__main__":
    list = [23, 89]
    threads = []
    # 创建4个线程
    for i in range(4):
        task = MyThread(add, (list[0], list[1]))
        task.start()
        threads.append(task)
    for t in threads:
        t.join()

    for t in threads:
        print t.get_result()
