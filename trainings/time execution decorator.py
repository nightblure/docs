import time

def time_exec(mode):
    def wrapper(func):
        def inner(*fargs, **fkwargs):
            start_time = time.monotonic()
            result = func(*fargs, **fkwargs)
            finish_time = time.monotonic() - start_time
            finish_time = finish_time * 1000 if mode == 'ms' else finish_time
            print(f'exec time of {func.__name__}: {round(finish_time, 2)} {mode}')
            return result
        return inner
    return wrapper
    
@time_exec('ms')
def test(*args):
    t = 1.5
    time.sleep(t)
    return t
    
# print(test(1, 5, 6))

# альтернативный способ вызова для демонстрации принципа работы декоратора
print(
    time_exec('ms')(test)(1, 5)
)
