# need to convert int to string without "str" method and etc.
def int_to_str(n: int):
    if n == 0:
        return "0"
    
    negative = False
    
    if n < 0:
        negative = True
        n = -n
    
    r = ''
    
    nums = range(10)
    m = dict(zip(nums, [str(x) for x in nums]))
    
    while n >= 1:
        last_num = n % 10
        r = "".join((m[last_num], r))
        n = n // 10
    
    return r if not negative else f"-{r}"


print(int_to_str(123), int_to_str(1230), int_to_str(1), int_to_str(-12), int_to_str(0))
