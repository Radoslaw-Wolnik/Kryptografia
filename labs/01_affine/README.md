# Lab 01 - Caesar and Affine Ciphers

This lab introduces classical substitution ciphers. These ciphers replace each plaintext letter
with another letter according to a simple rule.

## Concepts

The Caesar cipher shifts every letter by a fixed number:

```text
E(x) = x + k mod 26
D(y) = y - k mod 26
```

The affine cipher generalizes this by multiplying and then shifting:

```text
E(x) = a*x + b mod 26
D(y) = a^-1 * (y - b) mod 26
```

The important condition is that `a` must be invertible modulo 26. That means `gcd(a, 26) == 1`.
Without that condition, multiple plaintext letters collapse to the same ciphertext letter and the
cipher cannot be reversed.

## Implementation

Main implementation files:

- `src/kryptografia/classical/caesar.py`
- `src/kryptografia/classical/affine.py`
- `src/kryptografia/common/modular.py`
- `src/kryptografia/common/text.py`

The Caesar helpers implement encryption, decryption, and known-plaintext shift recovery. The
affine helpers implement encryption, decryption, and key recovery from matching plaintext and
ciphertext samples.

## Demo

Run:

```bash
python labs/01_affine/demo.py
```

The demo shows:

- Caesar encryption and decryption
- recovering a Caesar shift from known plaintext
- affine encryption and decryption
- recovering an affine key pair `(a, b)`
- rejecting an invalid affine key where `a` is not invertible

## Try It

- Change the Caesar shift to `13` and observe ROT13 behavior.
- Try affine keys such as `(7, 3)` or `(11, 4)`.
- Try `a=2` or `a=13` and explain why decryption is impossible.

