# Lab 03 - One-Time Pad and XOR

This lab introduces byte-wise XOR and the one-time pad. A true one-time pad encrypts by XORing
plaintext bytes with a random key of exactly the same length.

## Concepts

XOR has three useful properties:

```text
a xor a = 0
a xor 0 = a
(plaintext xor key) xor key = plaintext
```

If the key is uniformly random, as long as the plaintext, kept secret, and never reused, the
one-time pad has perfect secrecy.

The dangerous part is key reuse. If two messages use the same key:

```text
C1 = P1 xor K
C2 = P2 xor K
C1 xor C2 = P1 xor P2
```

The key disappears, leaking a relationship between the two plaintexts.

## Implementation

Main implementation files:

- `src/kryptografia/one_time_pad/xor.py`
- `src/kryptografia/common/xor.py`
- `src/kryptografia/common/text.py`

The package exposes equal-length XOR, repeating-key XOR, random key generation, OTP encrypt and
decrypt helpers, and escaped byte rendering for lab-friendly output.

## Demo

Run:

```bash
python labs/03_one_time_pad/demo.py
```

The demo shows:

- random OTP key generation
- byte encryption and decryption
- escaped rendering of non-printable bytes
- why reusing a key reveals `P1 xor P2`
- repeating-key XOR as an intentionally weaker construction

## Try It

- Encrypt two messages with the same key and compare `C1 xor C2`.
- Try messages of different lengths and see why equal-length XOR rejects them.
- Replace the random OTP key with a repeated short key and inspect the output pattern.

