from kryptografia.hashing import (
    change_password,
    check_credentials,
    dictionary_attack,
    hash_password,
    md5_hex,
    register_user,
)


def main() -> None:
    print("Lab 05 - Hashing, dictionary attacks, and credentials")
    print("=" * 57)

    dictionary = ["password", "hello", "cryptography", "secret"]
    target = md5_hex("secret")
    result = dictionary_attack(target, dictionary)

    print("\n1. Dictionary attack against an MD5 hash")
    print(f"target hash:      {target}")
    print(f"dictionary:       {dictionary}")
    print(f"best guess:       {result.guess}")
    print(f"similarity:       {round(result.similarity, 2)}%")
    print(f"exact match:      {result.exact_match}")

    print("\n2. Credential store as pure data, no socket/server side effects")
    records = register_user([], "alice", "correct horse", salt="lab")
    print(f"stored hash:      {records[0].password_hash}")
    print(f"manual hash:      {hash_password('correct horse', 'lab')}")
    print(f"login ok:         {check_credentials(records, 'alice', 'correct horse')}")
    print(f"wrong password:   {check_credentials(records, 'alice', 'wrong')}")

    records = change_password(records, "alice", "correct horse", "new secret")
    print(f"old password ok:  {check_credentials(records, 'alice', 'correct horse')}")
    print(f"new password ok:  {check_credentials(records, 'alice', 'new secret')}")


if __name__ == "__main__":
    main()

