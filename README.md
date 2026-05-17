# Kryptografia

Educational cryptography laboratory code refactored into one cohesive Python package.

This repository started as a set of university lab scripts. It is now organized as a small
educational codebase with reusable modules, lab demos, tests, and documentation. The goal is not
to provide production cryptography. The goal is to make the algorithms visible, testable, and easy
to discuss.

## What This Repository Teaches

The labs move from classical ciphers to public-key cryptography and steganography:

1. Caesar and affine substitution ciphers
2. Vigenere encryption and basic cryptanalysis
3. One-time pad, XOR, and key reuse mistakes
4. Padding, toy block ciphers, and block modes
5. Hash functions, similarity, dictionary attacks, and credential storage
6. Euclid, modular inverses, Euler phi, CRT, and primality checks
7. RSA over integers and byte blocks
8. Educational RSA signatures
9. Message integrity with digests
10. LSB and whitespace steganography

Most modules intentionally keep the implementation close to the math. That makes the code useful
for learning, debugging, and explaining each idea line by line.

## Repository Layout

```text
src/kryptografia/
  common/          shared text, byte, encoding, validation, XOR, and modular helpers
  classical/       Caesar, affine, Vigenere, and Vigenere analysis helpers
  one_time_pad/    OTP encryption, key generation, and escaped byte formatting
  block_ciphers/   PKCS#7 padding, XOR block demo, and Mini-DES style modes
  hashing/         hash comparison, dictionary attack, and credential workflows
  number_theory/   Euclid, modular inverse, CRT, Euler phi, primality checks
  rsa/             RSA integer operations plus byte/text block encoding
  signatures/      SHA-256 digest, integrity checks, textbook RSA signatures
  steganography/   LSB byte embedding and HTML whitespace embedding

labs/              runnable lab walkthroughs
tests/             repository-level verification
docs/              architecture and longer notes
experiments/       generated outputs, benchmarks, and exploratory material
```

The canonical source tree is `src/kryptografia`. Lab scripts should import from that package
rather than redefining algorithms locally.

## Setup

Create and activate a virtual environment, then install the project in editable mode:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Run the verification suite:

```bash
pytest
ruff check src tests labs
mypy src/kryptografia
```

Run a lab demo:

```bash
python labs/07_rsa/demo.py
```

If you do not install the package, set `PYTHONPATH=src` before running demos.

## Design Principles

- Reusable algorithm code lives in `src/kryptografia`.
- Lab files show examples, intermediate values, and learning context.
- Tests verify round trips, known answers, invalid inputs, and recovered values.
- Shared helpers prevent repeated implementations of GCD, modular inverse, XOR, encodings, and
  text handling.
- Dangerous simplifications are named clearly instead of hidden.

## Security Disclaimer

This is educational cryptography code. Do not use it to protect real data.

The implementations omit many properties required in real systems, including secure key
generation, authenticated encryption, side-channel resistance, hardened parsing, RSA padding,
signature padding, misuse-resistant APIs, and audited implementations. For production work, use
well-reviewed libraries such as `cryptography`, OpenSSL, libsodium, or platform security APIs.

