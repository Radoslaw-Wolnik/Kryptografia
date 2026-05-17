# Lab 07 - RSA

This lab introduces RSA, a public-key cryptosystem based on modular exponentiation and the
difficulty of factoring large composite numbers.

## Concepts

RSA key generation starts with two primes `p` and `q`:

```text
n = p*q
phi(n) = (p - 1)*(q - 1)
```

Choose a public exponent `e` such that `gcd(e, phi(n)) == 1`. The private exponent `d` is the
modular inverse of `e`:

```text
e*d = 1 mod phi(n)
```

Encryption and decryption are modular exponentiations:

```text
c = m^e mod n
m = c^d mod n
```

The lab also includes byte-wise text block helpers. They are useful for demonstrating how text can
be transformed into integer blocks, encrypted, serialized, decoded, and decrypted.

## Implementation

Main implementation files:

- `src/kryptografia/rsa/core.py`
- `src/kryptografia/rsa/blocks.py`
- `src/kryptografia/number_theory/euclid.py`
- `src/kryptografia/common/modular.py`

The implementation assumes supplied primes. It does not generate secure primes and does not use
real RSA padding.

## Demo

Run:

```bash
python labs/07_rsa/demo.py
```

The demo shows:

- small RSA key construction from `p=61` and `q=53`
- integer encryption and decryption
- byte-wise text encryption
- base64 serialization of encrypted integer blocks

## Try It

- Change the message integer and ensure it stays smaller than `n`.
- Try `p == q` and observe why it is rejected.
- Encrypt a short text string and inspect the encoded block list.

## Security Note

Textbook RSA is not secure. Real RSA needs secure prime generation, padding schemes such as OAEP
for encryption or PSS for signatures, and careful implementation practices.

