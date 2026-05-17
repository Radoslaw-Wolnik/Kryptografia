from kryptografia.signatures import sha256_hex, verify_message_integrity


def main() -> None:
    print("Lab 09 - Message integrity")
    print("=" * 28)

    original = "hello"
    received_ok = "hello"
    received_tampered = "hullo"

    print("\n1. Compare identical messages")
    print(f"original hash:    {sha256_hex(original)}")
    print(f"received hash:    {sha256_hex(received_ok)}")
    print(f"integrity ok:     {verify_message_integrity(original, received_ok)}")

    print("\n2. Detect a one-character change")
    print(f"tampered hash:    {sha256_hex(received_tampered)}")
    print(f"integrity ok:     {verify_message_integrity(original, received_tampered)}")
    print("\nA digest detects accidental or malicious change, but it does not prove who sent it.")


if __name__ == "__main__":
    main()

