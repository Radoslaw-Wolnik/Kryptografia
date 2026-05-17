# Lab 02 - Vigenere Cipher

This lab studies polyalphabetic substitution. Instead of using one fixed shift, Vigenere uses a
repeating keyword to select a different Caesar shift for each plaintext letter.

## Concepts

For a key such as `LEMON`, each key letter becomes a shift:

```text
L -> 11
E -> 4
M -> 12
O -> 14
N -> 13
```

The shifts repeat across the message. This hides single-letter frequency patterns better than a
Caesar cipher, but repeated keys still leak structure.

Kasiski examination looks for repeated substrings in the ciphertext. If the same plaintext segment
is encrypted under the same key alignment, repeated ciphertext segments can appear. Distances
between those repeats often share factors with the key length.

Frequency analysis then treats each key column as a Caesar cipher and scores possible shifts
against expected English letter frequencies.

## Implementation

Main implementation file:

- `src/kryptografia/classical/vigenere.py`

Shared helpers:

- `src/kryptografia/common/text.py`

Implemented operations include:

- `vigenere_encrypt`
- `vigenere_decrypt`
- `repeated_substrings`
- `kasiski_candidate_key_lengths`
- `guess_vigenere_key`
- `dictionary_attack`

## Demo

Run:

```bash
python labs/02_vigenere/demo.py
```

The demo shows:

- encryption and decryption with a keyword
- repeated substring discovery
- candidate key length estimation
- frequency-based key guessing
- a local dictionary-style key search

## Try It

- Replace the key with a shorter key and compare the Kasiski output.
- Use a very short ciphertext and observe how frequency guessing becomes unreliable.
- Add your own candidate keys to the dictionary attack list.

