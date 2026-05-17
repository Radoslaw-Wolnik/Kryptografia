# Architecture

The repository follows a single-package architecture:

```text
labs -> src/kryptografia modules -> common and number_theory foundations
```

The package is intentionally small. It is not trying to hide the algorithms behind heavy
frameworks. Instead, each module owns one educational topic and exposes functions that are easy to
test from labs and unit tests.

## Dependency Direction

The intended dependency flow is:

```text
labs/
  import from
src/kryptografia/classical
src/kryptografia/one_time_pad
src/kryptografia/block_ciphers
src/kryptografia/hashing
src/kryptografia/rsa
src/kryptografia/signatures
src/kryptografia/steganography
  import from
src/kryptografia/common
src/kryptografia/number_theory
```

Package modules should not import from `labs`, `tests`, or experiments. Tests are consumers of the
package, not part of the package.

## Shared Foundations

`kryptografia.common` contains helpers that are useful across multiple labs:

- `modular.py`: `gcd`, `extended_gcd`, `mod_inverse`, and modular normalization
- `xor.py`: equal-length XOR and repeating-key XOR
- `text.py`: ASCII alphabet helpers and escaped byte rendering
- `encodings.py`: text, bytes, and bit-string conversion
- `bytes.py`: byte chunking and zero padding
- `validation.py` and `exceptions.py`: small shared validation layer

`kryptografia.number_theory` builds on these helpers with concepts used by RSA and modular
arithmetic labs:

- Euler phi
- Chinese remainder theorem
- fast modular exponentiation
- Fermat and AKS-style primality checks

## Topic Modules

`classical` contains Caesar, affine, and Vigenere ciphers. It also includes Kasiski-style repeated
substring analysis and simple frequency-based Vigenere key guessing.

`one_time_pad` contains equal-length OTP operations over bytes. It deliberately exposes byte-level
operations because OTP correctness depends on exact key length and key reuse rules.

`block_ciphers` contains PKCS#7 padding, an intentionally insecure XOR block transformation, and a
Mini-DES style bit-block exercise with ECB, CBC, OFB, and CTR modes.

`hashing` contains hash normalization, MD5 similarity exercises, dictionary attack helpers, and a
pure in-memory credential workflow. The credential code avoids sockets and data files so it can be
tested deterministically.

`rsa` contains small integer RSA, plus helpers for serializing byte-wise RSA blocks to base64. It
assumes supplied primes in the simple key-generation function.

`signatures` contains SHA-256 digest helpers, digest comparison, and textbook-RSA style signatures.
The signatures intentionally omit real-world padding.

`steganography` contains two families of hiding techniques: LSB embedding in bytes and line-ending
whitespace embedding for text or HTML carriers.

## Tests

Tests live in `tests/` and are organized by lab topic. They cover:

- round trips, such as encrypt then decrypt
- known answer checks, such as a Caesar or MD5 expected result
- invalid-input behavior
- recovery helpers, such as Caesar and affine key recovery
- educational attacks, such as dictionary attack and Vigenere key guessing

The tests are intentionally direct. They should make it obvious what concept failed when something
breaks.

## What Was Not Preserved

The original repository included generated spreadsheets, images, PBM/PNG outputs, IDE metadata,
and old monolithic scripts. The cleaned repository preserves the useful educational behavior in
modules, demos, and tests, but it does not keep generated artifacts as source code.

