from gintro import Stream, timeit


a = [1,2,3]

@timeit
def double(a):
     return Stream(a).map(lambda x: x * 2).tolist()

print(double(a))

