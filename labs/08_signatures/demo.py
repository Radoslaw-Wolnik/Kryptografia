from kryptografia.rsa import generate_rsa_keypair
from kryptografia.signatures import rsa_sign, rsa_verify, sha256_hex


def main() -> None:
    print("Lab 08 - Educational digital signatures")
    print("=" * 43)

    keys = generate_rsa_keypair(61, 53, e=17)
    message = "signed lab message"
    signature = rsa_sign(message, keys.private_exponent, keys.modulus)

    print("\n1. Digest")
    print(f"message:          {message}")
    print(f"sha256:           {sha256_hex(message)}")

    print("\n2. Textbook-RSA signature")
    changed_valid = rsa_verify("changed", signature, keys.public_exponent, keys.modulus)
    print(f"signature integer:{signature}")
    print(f"valid message:    {rsa_verify(message, signature, keys.public_exponent, keys.modulus)}")
    print(f"changed message:  {changed_valid}")
    print("\nThis intentionally omits production signature padding.")


if __name__ == "__main__":
    main()
