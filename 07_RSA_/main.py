from RSA import RSA
from podpis_RSA import podpis_RSA

if __name__ == '__main__':
    print("RSA")

    szyfruj = RSA(n=10)
    print(szyfruj)

    msg = "Hello World!\nHello hello\n"
    msg= "3e359957ecf0e69cf068d2566848e3d5"
    # msg = "Howdy"
    # temp = szyfruj.cipher_blocks(msg, 1, 740813, 483031)
    # print(temp)

    ciphered_msg = szyfruj.cipher(msg)
    print(ciphered_msg)

    deciphered_msg = szyfruj.decipher(ciphered_msg)
    print(deciphered_msg)

    podpis = podpis_RSA()
    podpis.set_rsa(szyfruj)
    podpis.set_file("out.txt")
    # podpisane = podpis.sign()

    # podpis.verify(podpisane, szyfruj.get_public_key())



