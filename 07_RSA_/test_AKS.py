def coef(n):
    c = []
    c.append(1)
    for i in range(n):
        c.append(1)
        for j in range(i, 0, -1):
            c[j] = c[j - 1] - c[j]
        c[0] = -c[0]
    return c


def AKS(n):
    c = coef(n)
    c[0] = c[0] + 1
    c[-1] = c[-1] - 1
    i = n
    for a in c:
        if a % n != 0:
            return False
    return True


number = int(input())

result = AKS(number)
if result:
    print("Liczba pierwsza")
else:
    print("Liczba złożona")
