# Labs

This directory contains runnable demonstrations for each cryptography lab.

The demos are not the implementation source of truth. They are learning scripts that import from
`src/kryptografia`, build example inputs, show intermediate values, and print results that connect
the code to the cryptography concept.

## How To Run

After installing the package with `python -m pip install -e ".[dev]"`, run any demo directly:

```bash
python labs/01_affine/demo.py
python labs/07_rsa/demo.py
python labs/10_steganography/demo.py
```

Without installation, run with `PYTHONPATH=src`:

```bash
PYTHONPATH=src python labs/02_vigenere/demo.py
```

## Lab Structure

Each lab folder contains:

- `README.md`: concept explanation, implementation map, and exercises to try
- `demo.py`: runnable walkthrough using the package functions

Reusable logic belongs in `src/kryptografia`, not in `labs`. If a demo grows a new useful function,
move that function into the package and test it.

## Current Lab Map

| Lab | Topic | Main package modules |
| --- | --- | --- |
| 01 | Caesar and affine ciphers | `kryptografia.classical` |
| 02 | Vigenere and cryptanalysis | `kryptografia.classical.vigenere` |
| 03 | OTP and XOR | `kryptografia.one_time_pad`, `kryptografia.common.xor` |
| 04 | Block ciphers and modes | `kryptografia.block_ciphers` |
| 05 | Hashing and credentials | `kryptografia.hashing` |
| 06 | Number theory | `kryptografia.number_theory` |
| 07 | RSA | `kryptografia.rsa` |
| 08 | Digital signatures | `kryptografia.signatures` |
| 09 | Message integrity | `kryptografia.signatures.integrity` |
| 10 | Steganography | `kryptografia.steganography` |

