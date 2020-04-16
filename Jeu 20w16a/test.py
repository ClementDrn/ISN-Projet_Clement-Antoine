class A:
    def __init__(self):
        self.dict = {"a": {"A": 8, "AA": 80}, "b": {"B": 1, "BB": 10}, "c": {"C": 2, "CC": 20}}

    def func(self):
        for k1 in self.dict:
            for k2 in self.dict[k1]:
                if k1 == "a":
                    break
                else:
                    print(self.dict[k1][k2])


objA = A()
objA.func()