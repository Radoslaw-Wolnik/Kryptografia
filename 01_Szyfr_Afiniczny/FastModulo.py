class FastModulo:
    """korzystajac z rozszerzonego algorytmu potegowania modulo
    i reprezentacji liczby binarnej
    A^2 mod C = (A * A)mod C = ((A mod C) * (A mod C))mod C
    A^4 mod C = (A^2 * A^2)mod C = ((A^2 mod C) * (A^2 mod C))mod C
    zatem wyznaczamy binary repr of A 0bA = [1,0,0,1,0]
    liczymy potegi A^1 mod C, A^2 mod C, A^4 mod C, ...
    mnozymy wszysko dla 1 nie dla 0 i modulo"""

    def __init__(self, base=1, power=1, mod=1):
        self.base = base
        self.power = power
        self.mod = mod

    def change(self, base, power, mod):
        self.base = base
        self.power = power
        self.mod = mod

    def execute(self):
        temp = list(bin(self.power)[2::])
        binary = [int(el) for el in temp]
        power_list = [self.base % self.mod]
        for i in range(len(binary) - 1):
            temp = (power_list[-1] * power_list[-1]) % self.mod
            power_list.append(temp)
        power_list.reverse()
        res = 1
        for i in range(len(binary)):
            if binary[i] == 1:
                res *= power_list[i]
        print(power_list, "\n", binary)
        return res % self.mod
