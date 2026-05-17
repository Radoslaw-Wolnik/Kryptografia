# Lab 04 - Block Ciphers

This lab studies block-oriented encryption ideas: padding, fixed-size blocks, and common modes of
operation. The implementation is deliberately small and educational, not secure.

## Concepts

Block ciphers transform fixed-size chunks of data. Real ciphers such as AES operate on fixed block
sizes, so arbitrary-length messages need padding.

PKCS#7 padding appends `N` bytes each with value `N`. If a message already fits the block size, a
full block of padding is added so unpadding is unambiguous.

Modes describe how blocks are connected:

- ECB encrypts each block independently and leaks repeated patterns.
- CBC XORs each plaintext block with the previous ciphertext block.
- OFB turns the block cipher into a stream generator.
- CTR encrypts a nonce plus counter and XORs the result with plaintext.

## Implementation

Main implementation files:

- `src/kryptografia/block_ciphers/padding.py`
- `src/kryptografia/block_ciphers/modes.py`
- `src/kryptografia/block_ciphers/mini_des.py`

The package includes:

- PKCS#7 padding and unpadding
- a toy XOR block transformation
- a Mini-DES style 12-bit Feistel exercise
- ECB, CBC, OFB, and CTR helpers for the Mini-DES exercise

## Demo

Run:

```bash
python labs/04_block_ciphers/demo.py
```

The demo shows:

- how padding changes message length
- how unpadding validates the padding bytes
- a reversible XOR block transformation
- Mini-DES style outputs for ECB, CBC, OFB, and CTR

## Try It

- Change the plaintext so it is exactly 16 bytes and observe the extra padding block.
- Encrypt repeated Mini-DES blocks with ECB and CBC and compare the outputs.
- Change the IV or nonce and observe which modes change their ciphertext.

