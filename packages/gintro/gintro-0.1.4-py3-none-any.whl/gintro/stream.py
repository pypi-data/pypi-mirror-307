from functools import reduce


class Stream:
    def __init__(self, obj):
        if type(obj) == int:
            self.iterable = range(obj)
        else:
            self.iterable = obj

    # transform
    def map(self, fn):
        self.iterable = map(fn, self.iterable)
        return self

    def filter(self, fn):
        self.iterable = filter(fn, self.iterable)
        return self

    def unique(self):
        self.iterable = list(set(self.iterable))
        return self

    # group
    def collect_list(self, key_fn=None):
        if key_fn is not None:
            self.iterable = map(lambda row: (key_fn(row), row), self.iterable)

        collect_dict = dict()
        for k, v in self.iterable:
            if k in collect_dict:
                collect_dict[k].append(v)
            else:
                collect_dict[k] = [v]
        self.iterable = collect_dict.items()
        return self

    def agg(self, agg_fn):
        res_dict = dict()
        for k, v_list in self.iterable:
            try:
                res_dict[k] = reduce(agg_fn, v_list)
            except:
                print(k, v_list)
        self.iterable = res_dict.items()
        return self

    def keys(self):
        self.iterable = map(lambda kv: kv[0], self.iterable)
        return self

    def values(self):
        self.iterable = map(lambda kv: kv[1], self.iterable)
        return self

    # execute
    def len(self):
        return len(list(self.iterable))

    def sum(self):
        return sum(list(self.iterable))

    def max(self):
        return max(list(self.iterable))

    def min(self):
        return min(list(self.iterable))

    def tolist(self):
        return list(self.iterable)

    def to_dict(self):
        return dict(self.iterable)

    def to_enum(self):
        return dict(enumerate(self.iterable))

    def head(self, num=3):
        lst = []
        for it in self.iterable:
            lst.append(it)
            if len(lst) > num:
                break
        return lst

    def quantile(self, p):
        """
        need self.iterable to be sortable
        """
        lst = sorted(self.iterable)
        return lst[int[len(lst) * p]]


