from RSA import RSA

if __name__ == '__main__':
    print("RSA")

    szyfruj = RSA(n=10)
    print(szyfruj)

    msg = "Hello World!\nHello hello"
    # msg = "Howdy"
    # temp = szyfruj.cipher_blocks(msg, 1, 740813, 483031)
    # print(temp)

    ciphered_msg = szyfruj.cipher(msg)
    print(ciphered_msg)

    deciphered_msg = szyfruj.decipher(ciphered_msg)
    print(deciphered_msg)
