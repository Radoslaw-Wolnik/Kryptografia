from kryptografia.number_theory import (
    aks_via_binomial,
    chinese_remainder,
    euler_phi,
    extended_gcd,
    fast_mod_exp,
    fermat_primality_test,
    gcd,
    mod_inverse,
)


def main() -> None:
    print("Lab 06 - Euclid, Euler, CRT, and primality checks")
    print("=" * 55)

    divisor, x, y = extended_gcd(240, 46)
    print("\n1. Euclidean algorithms")
    print(f"gcd(48, 18):             {gcd(48, 18)}")
    print(f"extended_gcd(240, 46):   {(divisor, x, y)}")
    print(f"identity check:          {240 * x + 46 * y}")
    print(f"inverse 17 mod 3120:     {mod_inverse(17, 3120)}")

    print("\n2. Euler phi and CRT")
    print(f"phi(9):                  {euler_phi(9)}")
    print(f"phi(10):                 {euler_phi(10)}")
    print(f"x=2 mod 3, 3 mod 5, 2 mod 7 -> {chinese_remainder([2, 3, 2], [3, 5, 7])}")

    print("\n3. Fast modular exponentiation and primality")
    print(f"7^128 mod 13:            {fast_mod_exp(7, 128, 13)}")
    print(f"Fermat says 13 prime:    {fermat_primality_test(13, bases=[2, 3])}")
    print(f"Fermat says 9 prime:     {fermat_primality_test(9, bases=[2])}")
    print(f"AKS-style check for 7:   {aks_via_binomial(7)}")


if __name__ == "__main__":
    main()

