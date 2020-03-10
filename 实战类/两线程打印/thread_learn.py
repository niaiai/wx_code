import threading

"""
创建两个线程，其中一个输出1-52，另外一个输出A-Z。输出格式要求：12A 34B 56C 78D 依次类推
"""


def number_print(lock1, lock2):
    for i in range(1, 52, 2):
        lock1.acquire()
        print("%d%d" % (i, i+1), end='')
        lock2.release()


def alpha_print(lock1, lock2):
    for alpha in range(26):
        lock2.acquire()
        print(chr(alpha + ord('A')), end=' ')
        lock1.release()


if __name__ == "__main__":
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    lock2.acquire()

    n = threading.Thread(target=number_print, args=(lock1, lock2))
    a = threading.Thread(target=alpha_print, args=(lock1, lock2))
    n.start()
    a.start()
