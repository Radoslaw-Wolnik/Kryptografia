from stegano import lsb
from stegano.lsb import generators
from PIL import Image
from time import time
import os


def hide_message(image_path, output_path, message) -> bool:
    try:
        # Wczytaj obraz
        image = Image.open(image_path)

        # Ukryj wiadomość bez generatora liczb pierwszych
        # secret_image = lsb.hide(image_path, message)
        # z generatorem
        secret_image = lsb.hide(image_path, message, generators.eratosthenes())

        # Zapisz obraz z ukrytą wiadomością
        secret_image.save(output_path)
        print(f"Tajna wiadomość została ukryta w obrazie {output_path}")
        return True
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return False


def reveal_message(image_path) -> str:
    try:
        # Odkryj wiadomość bez generatora liczb pierwszych
        # secret_message = lsb.reveal(image_path)
        # z generatorem liczb pierwszych
        secret_message = lsb.reveal(image_path, generators.eratosthenes())

        if secret_message:
            print(f"Tajna wiadomość: {secret_message}")
            return secret_message
        else:
            print("Nie znaleziono tajnej wiadomości w podanym obrazie.")
            return ''
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return ''


if __name__ == '__main__':
    print("Steganografia")
    # lsbset
    # generators.eratosthenes

    hide_message("res/Golden-Retriever-Puppy.jpg", "out/hidden2.png", 'Cryptography')
    reveal_message("out/hidden2.png")

    messages = ["a", "cryptography", "Tajna wiadomość: Cryptography",
                "Tajna wiadomość została ukryta w obrazie out/hidden2.png",
                "Tajna wiadomość została ukryta w obrazie out/hidden2.png Tajna wiadomość: Cryptography"]
    files = ["res/100kB.jpg", "res/1Mb.jpeg", "res/10Mb.jpg"]

    cipher_time = {key: [] for key in files}
    decipher_time = {key: [] for key in files}
    diff_in_size = {key: [] for key in files}
    for file in files:
        before_size = os.path.getsize(file)
        for mess in messages:
            start = time()
            hide_message(file, "out/temp.png", mess)
            finish = time()
            cipher_time[file].append(finish - start)

            start = time()
            reveal_message("out/temp.png")
            finish = time()
            decipher_time[file].append(finish - start)

            after_size = os.path.getsize("out/temp.png")

            diff_in_size[file].append(after_size - before_size)

    mess_len = [len(message) for message in messages]
    for key, val in cipher_time.items():
        print(f"Szyfrowanie czas dla pliku {key}")
        for i in range(len(val)):
            print(f'message lenght: {mess_len[i]} time: {val[i]}')
        print()

    for key, val in decipher_time.items():
        print(f"Deszyfrowanie czas dla pliku {key}")
        for i in range(len(val)):
            print(f'message lenght: {mess_len[i]} time: {val[i]}')
        print()

    for key, val in decipher_time.items():
        print(f"Zmiana wielkości dla pliku {key}")
        for i in range(len(val)):
            print(f'message lenght: {mess_len[i]} zmiana wielkości: {val[i]}')
        print()

# import stegano
# pip install stegano
