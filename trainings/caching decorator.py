import time

def cache():
    cache = {}
    def wrapper(f):
        def inner(*a, **kw):
            key = str((a, kw))
            
            if key not in cache:
                cache[key] = f(*a, **kw)
                
            return cache[key]
        return inner
    return wrapper

@cache()
def test(t=1.5, a=1):
    time.sleep(t)
    return 2

def main():
    for _ in range(10000):
        test(t=3)

start_time = time.monotonic()
main()
end_time = time.monotonic()
print(end_time - start_time)
