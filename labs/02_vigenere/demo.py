from kryptografia.classical import (
    dictionary_attack,
    guess_vigenere_key,
    kasiski_candidate_key_lengths,
    repeated_substrings,
    vigenere_decrypt,
    vigenere_encrypt,
)


def main() -> None:
    print("Lab 02 - Vigenere cipher and basic cryptanalysis")
    print("=" * 54)

    plaintext = (
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY "
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY "
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY"
    )
    key = "LEMON"
    ciphertext = vigenere_encrypt(plaintext, key)

    print("\n1. Encryption and decryption")
    print(f"key:              {key}")
    print(f"ciphertext sample:{ciphertext[:90]}...")
    print(f"round trip ok:    {vigenere_decrypt(ciphertext, key) == plaintext}")

    print("\n2. Kasiski examination")
    repeats = repeated_substrings(ciphertext, min_length=4, max_length=8)
    for substring, positions in list(repeats.items())[:5]:
        print(f"repeat {substring!r:<10} at positions {positions[:4]}")
    print(f"candidate lengths:{kasiski_candidate_key_lengths(ciphertext)[:8]}")

    print("\n3. Frequency-based key guess")
    guessed = guess_vigenere_key(ciphertext, len(key))
    print(f"guessed key:      {guessed}")
    print(f"decrypted sample: {vigenere_decrypt(ciphertext, guessed)[:90]}...")

    print("\n4. Dictionary attack with local candidate keys")
    candidates = ["DOG", "CIPHER", "LEMON", "SECRET"]
    print(f"candidates:       {candidates}")
    print(f"best key:         {dictionary_attack(ciphertext, candidates)}")


if __name__ == "__main__":
    main()

