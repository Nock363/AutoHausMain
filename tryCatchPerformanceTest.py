#test which python try catch is faster. in loop or outside loop
import timeit

n = 100000

def test1():
    for i in range(n):
        try:
            m = n*n
        except:
            pass

def test2():
    try:
        for i in range(n):
            m = n*n
    except:
        pass


if __name__ == '__main__':
    innerTest = timeit.timeit("test1()", setup="from __main__ import test1", number=10)
    outterTest =timeit.timeit("test2()", setup="from __main__ import test2", number=10)

    improvment = innerTest/outterTest

    print("Inner Try catch:",innerTest)
    print("Outter Try catch:",outterTest)
    print(f"Outter ist {improvment} mal schneller als Inner")
