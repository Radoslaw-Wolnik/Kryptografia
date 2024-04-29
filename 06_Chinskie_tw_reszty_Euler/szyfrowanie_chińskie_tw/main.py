

# ZADANIE 8

def gcd(a, b):
    """Function to find the greatest common divisor (GCD) using Euclid's algorithm."""
    while b != 0:
        a, b = b, a % b
    return a


def coprime(modulos):
    """Check if the given modulos are pairwise coprime."""
    n = len(modulos)
    for i in range(n):
        for j in range(i + 1, n):
            if gcd(modulos[i], modulos[j]) != 1:
                return False
    return True


def chinese_remainder_theorem(remainders, modulos):
    """
    Chinese Remainder Theorem implementation to find the value of 'a' that satisfies the system of equations.
    """
    assert len(remainders) == len(modulos), "The number of remainders must be equal to the number of modulos."

    if not coprime(modulos):
        return None

    M = 1
    for modulo in modulos:
        M *= modulo

    result = 0
    for i, remainder in enumerate(remainders):
        Mi = M // modulos[i]
        Mi_inv = pow(Mi, -1, modulos[i])
        result += remainder * Mi * Mi_inv

    return result % M


if __name__ == '__main__':
    print("Szyfrowanie za pomocą chińskiego twierdzenia o resztach")
    # changing input into correct format
    # mode = input()
    mode = "deszyfruj"  # "szyfruj" lub "deszyfruj"
    assert mode == "szyfruj" or mode == "deszyfruj", "Wskaż prawidłowy tryb (szyfruj | deszyfruj)"
    # M = input()
    M = "61 53"
    M = M.split()
    M = [int(num) for num in M]
    assert coprime(M), "given number of modulos must be prime to each other"
    # line3 = input()
    line3 = "32 23"  # or "2 45" in deszyfruj 1984
    result = None
    if mode == "szyfruj":
        number = int(line3)
        result = [number % mod for mod in M]
        result = " ".join([str(num) for num in result])
        # out: 2 45 | i think it should be 32, 23 for 1984 but im just a student
    if mode == "deszyfruj":
        A = line3.split()
        A = [int(num) for num in A]
        result = chinese_remainder_theorem(A, M)
        result = str(result)
        # out: 1984

    if result is None:
        print("Brak rozwiązania!!!")
    else:
        # print("Value of 'a' satisfying the system of equations:", result)
        print(result)
