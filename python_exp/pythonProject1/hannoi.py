# def move(n, a, b, c):
#     if(n == 1):
#         print(a,"->",c)
#         return
#     move(n-1, a, c, b)
#     move(1, a, b, c)
#     move(n-1, b, a, c)
# move(3, "a", "b", "c")
class Person(object):
    def shouru(self, wages):
        self._shouru = wages

    def display(self, res):
        print("sum of it is ", res)

class Student(Person):
    def __init__(self, awards):
        self._awards = awards
    def calculate(self):
        self.__init__()

class Staff(Person):
    def display(self,wages,awards):
        print("This is Staff!")
        res = wages*0.6+awards*0.4
        super.display(res)

