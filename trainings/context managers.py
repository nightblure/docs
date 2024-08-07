from contextlib import contextmanager
import asyncio

# FUNCTION
@contextmanager
def test():
    print('func before')
    yield
    print('func after')
    
with test():
    pass


# CLASS
class Test:
    async def __aenter__(self):
        print('class aenter')
        return self
    
    def test(self):
        pass
    
    async def __aexit__(self, *args):
        print('class aexit')

async def main():        
    obj = Test()
    
    async with obj:
        obj.test()
        
asyncio.run(main())
