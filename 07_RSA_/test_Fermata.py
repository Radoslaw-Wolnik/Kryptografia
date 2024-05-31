import random


def fast_modulo(base, power, mod):
    temp = list(bin(power)[2::])
    binary = [int(el) for el in temp]
    power = []
    power.append(base % mod)
    for i in range(len(binary) - 1):
        temp = (power[-1] * power[-1]) % mod
        power.append(temp)
    power.reverse()
    res = 1
    for i in range(len(binary)):
        if binary[i] == 1:
            res *= power[i]
    return res % mod


def gcd(x, y):
    # algorytm euclidesa
    while y > 0:
        x, y = y, x % y
    return x


def test_fermata(num):
    """-1 - liczba zlozona
    1 - liczba mby pierwsza"""
    losowa = random.randint(2, num - 1)
    divisor = gcd(num, losowa)
    if divisor > 1:
        return -1
    mod = fast_modulo(losowa, num - 1, num)
    if mod == 1:
        return 1
    return -1


# numbers = input()
numbers = "13 2 1"  # "9 2 1"
n, k, s = [int(n) for n in numbers.split(" ")]
random.seed(s)

result = 1
for i in range(k):
    test = test_fermata(n)
    if test != 1:
        result = -1
        break

if result == 1:
    print("Liczba prawdopodobnie pierwsza")
else:
    print("Liczba złożona")
