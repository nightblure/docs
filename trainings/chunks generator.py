def get_chunks(l, chunks_count: int):
    chunks_elements_count = len(l) // chunks_count
    
    for offset in range(0, len(l), chunks_elements_count):
        yield l[offset: offset + chunks_elements_count]


def get_chunks_by_elems_count(l, elements_count: int):
    for offset in range(0, len(l), elements_count):
        yield l[offset: offset + elements_count]
      

N = 40
l = list(range(1, N + 1))

g = get_chunks(l, 4)

for c in g:
    print(c)
