def print_object(obj):
    #print(f'{str(obj)}:', end=' ')
    if isinstance(obj, dict):
        print(obj, end=' ')
    else:
        [print(x, end=' ') for x in obj if x]
    print()

# генераторное выражение
gen_expr = (x for x in range(1, 21) if x % 2 == 0)

# функция-генератор
def g_func():
    current = 1
    while current < 21:
        if current % 2 == 0:
            yield current
        current += 1

# протокол итератора
class Gen:
    def __init__(self):
        self.current_index = 0
        self.l = [x for x in range(1, 11)]
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_index > len(self.l) - 1:
            raise StopIteration
        
        value = self.l[self.current_index]
        self.current_index += 1
        return value
    
    def __name__():
        return cls.__name__

print_object(gen_expr)
           
g = g_func()
print_object(g)

obj = Gen()
print_object(obj)

s = {x for x in range(1, 21) if x % 2 == 0}
d = {x: x for x in range(1, 21) if x % 2 == 0}
l = [x for x in range(1, 21) if x % 2 == 0]
print_object(s)
print_object(d)
print_object(l)
