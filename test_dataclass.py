import random
from dataclasses import dataclass


A_CACHE = {}


@dataclass(frozen=True)
class A:
    a: int

    def __new__(cls, a):
        if a in A_CACHE:
            return A_CACHE[a]
        obj = super().__new__(cls)
        object.__setattr__(obj, "a", a)
        A_CACHE[a] = obj
        return obj



class ExtendA:
    def __init__(self, a: int, param: int) -> None:
        self.a = A(a)
        self.param = param


all_extendA = []
all_A = []

for i in range(100):
    extend_a = ExtendA(i, i)
    all_extendA.append(extend_a)
    all_A.append(extend_a.a)

for _ in range(10):
    a = A(random.randint(1, 100))

    print(a in all_A)
