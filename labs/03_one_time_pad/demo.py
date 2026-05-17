from kryptografia.common import repeating_key_xor, xor_bytes
from kryptografia.one_time_pad import EncodedBytes, generate_key, otp_decrypt, otp_encrypt


def main() -> None:
    print("Lab 03 - One-time pad, XOR, and key reuse")
    print("=" * 47)

    plaintext = b"attack at dawn"
    key = generate_key(len(plaintext))
    ciphertext = otp_encrypt(plaintext, key)

    print("\n1. Proper one-time-pad round trip")
    print(f"plaintext:        {plaintext}")
    print(f"key escaped:      {EncodedBytes(key).to_escape_string()}")
    print(f"cipher escaped:   {EncodedBytes(ciphertext).to_escape_string()}")
    print(f"decrypted:        {otp_decrypt(ciphertext, key)}")

    print("\n2. Why key reuse is dangerous")
    first = b"attack at dawn"
    second = b"defend at dusk"
    reused_key = b"\x10" * len(first)
    first_cipher = otp_encrypt(first, reused_key)
    second_cipher = otp_encrypt(second, reused_key)
    xor_of_ciphers = xor_bytes(first_cipher, second_cipher)
    xor_of_plaintexts = xor_bytes(first, second)
    print(f"C1 xor C2:        {EncodedBytes(xor_of_ciphers).to_escape_string()}")
    print(f"P1 xor P2:        {EncodedBytes(xor_of_plaintexts).to_escape_string()}")
    print(f"same value:       {xor_of_ciphers == xor_of_plaintexts}")

    print("\n3. Repeating-key XOR is convenient but not an OTP")
    repeated = repeating_key_xor(b"educational example", b"ICE")
    print("key:              ICE")
    print(f"cipher hex:       {repeated.hex()}")


if __name__ == "__main__":
    main()

