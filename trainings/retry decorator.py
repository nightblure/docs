import time

def retry(retries=3, timeout=1):
    def wrapper(f):
        def inner(*a, **kw):
            cur = 0
            
            while cur < retries:
                try:
                    return f(*a, **kw)
                except Exception as e:
                    cur += 1
                    print(f'retry №{cur}...')
                    time.sleep(timeout)
                    continue
                
            raise Exception('retry exception')
        return inner
    return wrapper

state_for_test = 1

@retry(5, 1)
def test():
    global state_for_test
    
    if state_for_test == 3:
        return 'success'
        
    state_for_test += 1
    x = 1 / 0
    
test()
    
