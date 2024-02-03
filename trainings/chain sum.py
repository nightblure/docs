
def chain_sum(n):
    
    # chain_sum function "remember" about summ because return "inner" function
    summ = n
    
    def inner(n=None):
        nonlocal summ
        
        if n is None:
            return summ
            
        summ += n
        return inner
    
    return inner

print(
    chain_sum(4)(-3)(),
    chain_sum(-5)(),
    chain_sum(-1)(1)(5)()
)
