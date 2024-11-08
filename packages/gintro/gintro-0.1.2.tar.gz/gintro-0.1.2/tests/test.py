from gintro import Stream


a = [1,2,3]
b = Stream(a).map(lambda x: x * 2).tolist()

print(b)

