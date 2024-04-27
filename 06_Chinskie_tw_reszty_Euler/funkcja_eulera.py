# funkcja eulera
# ile jest liczb które coś tam coś tam eg liczba pierwsza tylko ona i jeden
# ile jest liczb względnie pierwszych do n
def gcd(a, b):
    """Funkcja znajdująca greatest common divisor (GCD) wykożystując algorytm euklidesa"""
    while b != 0:
        a, b = b, a % b
    return a

def prime_relative_numbers(n):
    """Funkcja wyznaczająca wszystkie liczby które są względnie pierwsze do danej liczby n"""
    prime_relative = []
    for i in range(1, n):
        if gcd(n, i) == 1:
            prime_relative.append(i)
    return prime_relative


# number = int(input())
number = 1200
prime_relative = prime_relative_numbers(number)
print(len(prime_relative))
print(" ".join([str(num) for num in prime_relative]))