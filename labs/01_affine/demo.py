from kryptografia.classical import (
    affine_decrypt,
    affine_encrypt,
    caesar_decrypt,
    caesar_encrypt,
    recover_affine_key,
    recover_caesar_shift,
)


def main() -> None:
    print("Lab 01 - Caesar and affine ciphers")
    print("=" * 42)

    plaintext = "Attack at Dawn!"
    caesar_shift = 3
    caesar_ciphertext = caesar_encrypt(plaintext, caesar_shift)
    recovered_shift = recover_caesar_shift(plaintext, caesar_ciphertext)

    print("\n1. Caesar cipher")
    print(f"plaintext:       {plaintext}")
    print(f"shift:           {caesar_shift}")
    print(f"ciphertext:      {caesar_ciphertext}")
    print(f"decrypted:       {caesar_decrypt(caesar_ciphertext, caesar_shift)}")
    print(f"known-text shift:{recovered_shift}")

    a, b = 5, 8
    affine_ciphertext = affine_encrypt(plaintext, a, b)
    recovered_key = recover_affine_key(plaintext, affine_ciphertext)

    print("\n2. Affine cipher")
    print("formula:         E(x) = (a*x + b) mod 26")
    print(f"key:             a={a}, b={b}")
    print(f"ciphertext:      {affine_ciphertext}")
    print(f"decrypted:       {affine_decrypt(affine_ciphertext, a, b)}")
    print(f"known-text key:  {recovered_key}")

    print("\n3. Invalid-key check")
    try:
        affine_encrypt("test", a=13, b=2)
    except ValueError as error:
        print(f"a=13 rejected:   {error}")


if __name__ == "__main__":
    main()

