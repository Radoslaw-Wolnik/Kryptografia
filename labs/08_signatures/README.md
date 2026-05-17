# Lab 08 - Digital Signatures

This lab demonstrates the idea behind digital signatures: a private key creates a value that a
public key can verify.

## Concepts

A signature is usually computed over a digest of the message rather than over the entire message.
The digest gives a fixed-size representation of the message content.

In this educational implementation:

```text
digest = SHA-256(message)
signature = digest^d mod n
verification checks signature^e mod n
```

This resembles RSA signing mathematically, but it omits the padding and encoding rules required in
real signatures.

## Implementation

Main implementation files:

- `src/kryptografia/signatures/digest.py`
- `src/kryptografia/signatures/rsa_signature.py`
- `src/kryptografia/rsa/core.py`

The package exposes:

- `sha256_hex`
- `rsa_sign`
- `rsa_verify`

## Demo

Run:

```bash
python labs/08_signatures/demo.py
```

The demo shows:

- SHA-256 digest calculation
- signing a message with the private exponent
- verifying with the public exponent
- verification failure after changing the message

## Try It

- Change the message after signing and check verification.
- Use a different RSA key pair.
- Compare this with Lab 09, where a digest detects change but does not prove who created it.

## Security Note

This is textbook RSA signing. Production RSA signatures need schemes such as RSA-PSS and a
well-reviewed cryptographic library.

