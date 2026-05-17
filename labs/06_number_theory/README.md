# Lab 06 - Number Theory

This lab collects the modular arithmetic used later by RSA and signatures.

## Concepts

Euclid's algorithm computes the greatest common divisor. The extended Euclidean algorithm also
finds coefficients `x` and `y` such that:

```text
a*x + b*y = gcd(a, b)
```

When `gcd(a, m) == 1`, this gives a modular inverse:

```text
a * a^-1 = 1 mod m
```

Euler's phi function counts how many numbers from `1` to `n` are coprime with `n`. For two primes
`p` and `q`, RSA uses:

```text
phi(p*q) = (p - 1) * (q - 1)
```

The Chinese remainder theorem solves systems of congruences with pairwise-coprime moduli.

## Implementation

Main implementation files:

- `src/kryptografia/common/modular.py`
- `src/kryptografia/number_theory/euclid.py`
- `src/kryptografia/number_theory/primality.py`

The package includes:

- GCD and extended GCD
- modular inverse
- coprime check
- Euler phi
- Chinese remainder theorem
- fast modular exponentiation
- Fermat primality test
- small AKS-style educational primality check

## Demo

Run:

```bash
python labs/06_number_theory/demo.py
```

The demo shows:

- Euclidean algorithm results
- extended GCD identity verification
- modular inverse
- Euler phi examples
- CRT solving
- fast modular exponentiation
- simple primality checks

## Try It

- Compute `mod_inverse(3, 26)` and compare it with affine cipher keys.
- Try CRT with non-coprime moduli and observe the validation error.
- Run the AKS-style check only for small numbers; it is intentionally inefficient.

