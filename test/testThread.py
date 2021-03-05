#coding=utf-8

import threading, time

threads = []
# lock = threading.Lock()  # 生成全局锁

num = []  # 共享变量
def func():
    global num
    num.append(1)
    num.pop(0)
    time.sleep(0.1)
    return -1

threads = []
for i in range(100):
    t = threading.Thread(target=func)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print num