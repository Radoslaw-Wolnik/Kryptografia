# Lab 10 - Steganography

This lab studies hiding data inside a carrier. Unlike encryption, steganography tries to hide the
existence of a message.

## Concepts

Least-significant-bit steganography changes the lowest bit of carrier bytes. For many media types,
small low-bit changes may be hard to notice visually, though this repository demonstrates the idea
with raw bytes rather than a full image pipeline.

Whitespace steganography hides bits in text formatting. In the line-ending variant:

- no trailing space means bit `0`
- one trailing space means bit `1`

This mirrors the original HTML-oriented lab idea while keeping the implementation pure and easy to
test.

## Implementation

Main implementation files:

- `src/kryptografia/steganography/lsb.py`
- `src/kryptografia/steganography/html_whitespace.py`

The package includes:

- text-to-bit and bit-to-text conversion
- LSB message embedding and extraction
- hexadecimal message conversion to bits
- line-ending whitespace embedding and extraction

## Demo

Run:

```bash
python labs/10_steganography/demo.py
```

The demo shows:

- embedding a text message into byte least-significant bits
- counting how many carrier bytes changed
- extracting the hidden message
- embedding a hexadecimal message into line-ending whitespace
- extracting the hidden hexadecimal message

## Try It

- Reduce the byte carrier size and observe the capacity error.
- Change the hidden message and count how many bytes are modified.
- Open the whitespace carrier in an editor that shows trailing spaces.

## Security Note

These methods are fragile. Compression, formatting, image conversion, minification, or cleanup
tools can destroy the hidden message.

