# Lab 09 - Message Integrity

This lab focuses on detecting message changes with digests.

## Concepts

Integrity means that data has not changed. A hash digest can detect changes because even a small
edit should produce a very different digest.

However, a plain digest does not authenticate the sender. Anyone can compute a digest for a new
message. Authentication requires something secret or private, such as a MAC key or a digital
signature.

This lab deliberately separates these ideas:

- Lab 09: detect whether two messages match
- Lab 08: verify a message using a public key and signature

## Implementation

Main implementation files:

- `src/kryptografia/signatures/digest.py`
- `src/kryptografia/signatures/integrity.py`

The key function is:

```python
verify_message_integrity(original, received)
```

It hashes both inputs with SHA-256 and compares the hexadecimal digests.

## Demo

Run:

```bash
python labs/09_integrity/demo.py
```

The demo shows:

- identical messages producing the same digest
- a one-character change producing a different digest
- why digest comparison is useful but not the same as authentication

## Try It

- Change `hello` to `Hello` and compare the hashes.
- Try a longer message with punctuation and whitespace changes.
- Think about why an attacker could replace both the message and its plain digest.

