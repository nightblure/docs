import time
from collections import deque


def g1():
    x = 1
    while x <= 3:
        print('some work g1...')
        time.sleep(0.3)
        yield
        x += 1


def g2():
    x = 1
    while x <= 6:
        print('some work g2...')
        time.sleep(0.5)
        yield
        x += 1
    

def eventloop(queue):
    while len(queue) > 0:
        coroutine = queue.popleft()
        
        try:
            next(coroutine)
        except StopIteration:
            continue
        
        queue.append(coroutine)
        
    print('eventloop complete')


queue = deque([g1(), g2()])
eventloop(queue)
        
        
