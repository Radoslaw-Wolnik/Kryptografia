# put your python code here
# brakuje testu 3 - Program ma uwzględnić przypadek, kiedy zbiór m1,…,mrm1​,…,mr​ nie jest względnie pierwszy
# https://math.stackexchange.com/questions/1095442/chinese-remainder-theorem-for-non-prime-non-coprime-moduli
# https://math.stackexchange.com/questions/120070/chinese-remainder-theorem-with-non-pairwise-coprime-moduli

def gcd(a, b):
    """Function to find the greatest common divisor (GCD) using Euclid's algorithm."""
    while b != 0:
        a, b = b, a % b
    return a


def coprime(modulos):
    """Check if the given modulos are pairwise coprime."""
    if modulos is None:
        return False
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


def gcd_list(numbers):
    if not numbers:
        return None  # If the list is empty, there's no common divisor
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result


def reprime(A, M):
    mod = gcd_list(M)
    if mod == 1:
        return None, A
    same = [a % mod for a in A]
    is_the_same = same[0]  # some number that we will be comparing to
    for i in range(len(same)):
        if same[i] != same[0]:
            is_the_same = -1  # False
            break
    if is_the_same < 0:
        return None, A
    # zeby zrobic w petli to na pierwsze miejsce bierzemy ostatni element, potem (pierwszy element / gcd(list)) i potem reszte listy
    if len(M) > 2:
        return [M[-1]] + [M[0] / mod] + M[1:-1], [A[-1], A[0]] + A[1:-1]
    else:
        return [M[-1]] + [M[0] / mod], [A[-1], A[0]]


if __name__ == '__main__':
    print("Chińskie twierdzenie o restach i Euclides i Euler i liczby względnie pierwsze")
    # changing input into correct format
    # A = input()
    # M = input()
    # A = A.split()
    # M = M.split()
    # 
    # A = [int(num) for num in A]
    # M = [int(num) for num in M]
    A = [2, 3, 5]
    M = [3, 5, 7]
    result = None
    if coprime(M) is False:
        M, A = reprime(A, M)
        while not coprime(M):
            if M is None:
                break
            M, A = reprime(A, M)
        if M is not None:
            result = chinese_remainder_theorem(A, M)
    else:
        result = chinese_remainder_theorem(A, M)
    if result is None:
        print("Brak rozwiązania!!!")
    else:
        # print("Value of 'a' satisfying the system of equations:", result)
        print(result)
