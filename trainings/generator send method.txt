def gen_func():
    while True:
        x = yield
        x += 5
        print(x)

g = gen_func()
g.send(None)
g.send(3)
g.send(6)
