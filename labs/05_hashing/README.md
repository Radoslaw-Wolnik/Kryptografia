# Lab 05 - Hashing

This lab covers hash functions, digest comparison, dictionary attacks, and simple credential
storage. Hashes are one-way summaries of data: small changes in input should produce very different
digests.

## Concepts

A cryptographic hash function maps arbitrary data to a fixed-size digest. Good hash functions are
designed to resist preimage, second-preimage, and collision attacks.

This lab uses MD5 for historical and educational comparison exercises. MD5 is broken for
cryptographic security and should not be used in real systems.

Dictionary attacks try likely plaintexts, hash each candidate, and compare the result with a
target hash. This is why password storage needs slow password hashing and salts in real systems.

## Implementation

Main implementation files:

- `src/kryptografia/hashing/similarity.py`
- `src/kryptografia/hashing/dictionary_attack.py`
- `src/kryptografia/hashing/credentials.py`

The package includes:

- hexadecimal hash normalization
- hash-to-bit-string conversion
- bit similarity percentage
- MD5 digest helper
- dictionary attack helper
- pure in-memory credential registration, login check, and password change workflow

## Demo

Run:

```bash
python labs/05_hashing/demo.py
```

The demo shows:

- computing a target MD5 digest
- trying candidate dictionary words
- reporting the best match and exact match status
- storing a salted password hash in a small in-memory credential list
- checking login and changing a password

## Try It

- Add more candidate words to the dictionary list.
- Compare hashes for `secret` and `Secret`.
- Register the same username twice and inspect the error behavior.

