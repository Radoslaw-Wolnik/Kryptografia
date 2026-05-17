from kryptografia.rsa import (
    decode_cipher_blocks,
    encode_cipher_blocks,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_decrypt_text,
    rsa_encrypt,
    rsa_encrypt_text,
)


def main() -> None:
    print("Lab 07 - RSA integers and text blocks")
    print("=" * 40)

    keys = generate_rsa_keypair(61, 53)
    message = 42
    ciphertext = rsa_encrypt(message, keys.public_exponent, keys.modulus)

    print("\n1. Integer RSA")
    print("p, q:             61, 53")
    print(f"n:                {keys.modulus}")
    print(f"public e:         {keys.public_exponent}")
    print(f"private d:        {keys.private_exponent}")
    print(f"message:          {message}")
    print(f"ciphertext:       {ciphertext}")
    print(f"recovered:        {rsa_decrypt(ciphertext, keys.private_exponent, keys.modulus)}")

    print("\n2. Text encoded as one-byte RSA blocks")
    text = "Hello RSA!"
    encoded = rsa_encrypt_text(text, keys.public_exponent, keys.modulus)
    print(f"text:             {text}")
    print(f"base64 blocks:    {encoded}")
    print(f"decoded blocks:   {decode_cipher_blocks(encoded, keys.modulus)}")
    print(f"recovered text:   {rsa_decrypt_text(encoded, keys.private_exponent, keys.modulus)}")

    print("\n3. Block serialization")
    blocks = [1, 255, 1024]
    packed = encode_cipher_blocks(blocks, keys.modulus)
    print(f"blocks:           {blocks}")
    print(f"packed:           {packed}")
    print(f"unpacked:         {decode_cipher_blocks(packed, keys.modulus)}")


if __name__ == "__main__":
    main()

