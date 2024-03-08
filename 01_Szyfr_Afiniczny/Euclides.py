class Euclides():

    def __init__(self):
        pass

    def gcd(self, x, y):
        """Euclidian alghoritm
        To find greatest common divider - gcd"""
        while y > 0:
            x, y = y, x % y
        return x

    def xgcd(self, a, b):
        """"Extended euclidian alghoritm
        to find element opposite to {a} in an integer ring of {b} - base
        witch is t[-2]"""
        assert type(a) != int or type(b) != int, "Elements passed to function should be int"
        a, b = max(a, b), min(a, b)

        q = [-1, -1]
        r = [a, b]
        s = [1, 0]
        t = [0, 1]

        while r[-1] > 0:
            q.append(r[-2] // r[-1])
            r.append(r[-2] % r[-1])
            s.append(s[-2] - q[-1] * s[-1])
            t.append(t[-2] - q[-1] * t[-1])

        return s[-2], t[-2]
