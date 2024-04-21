import hashlib
import requests
import math
import pandas as pd
import time
from openpyxl.workbook import Workbook


def dictionary_attack_hash(hash, salt, english_dictionary):
    # because of usage of salt rainbow tables are useless
    # rainbow tables - tables of precomputed hashes for many many words
    ciphered = hash
    mdC = hashlib.md5(ciphered.encode('utf-8'))  # here add salt if salted
    binC = bin(int.from_bytes(mdC.digest(), byteorder='big'))[2:]
    C = binC.zfill(128)

    result = ""
    highest = 0
    for word in english_dictionary:

        mdN = hashlib.md5(word.encode('utf-8'))  # add salt here if salted
        binN = bin(int.from_bytes(mdN.digest(), byteorder='big'))[2:]
        N = binN.zfill(128)

        same_bits = [1 if C[i] == N[i] else 0 for i in range(len(C))]
        similarity = (sum(same_bits) / len(N)) * 100

        if math.ceil(similarity) == 100:
            result = word
            break

        if math.ceil(similarity) > highest:
            highest = similarity
            result = word

    print(f'haslo: {result} odniosło poziom poprawności: {highest}')
    return result, highest


if __name__ == '__main__':
    print("Funkcje skrotu")
    # server done
    # client done

    # username : password
    # Radek : Radek
    # Julia : Amelia
    # Kasia : Kasia
    df = pd.read_csv("server/user_credentials.csv")
    if not df.empty:
        # Understanding dataframe contest
        # All columns in our csv file
        print(df.columns)
        # First 3 entries
        print(df.head(3))
        # Entire first - 0 row
        print(df.iloc[0])

    r = None
    try:
        r = requests.get("https://stepik.org/media/attachments/lesson/668860/dictionary.txt")
    except ConnectionError:
        print("Connection failure")
    except Exception as e:
        print(f"Unexpected {e = }\n{type(e) = }")

    # database = [ (hashed_password, used_salt), (,), .... ]
    df = pd.read_csv('server/user_credentials.csv')  # Replace 'your_file.csv' with the path to your CSV file
    database = [(row['Password'], row['Salt'], row['Username']) for index, row in df.iterrows()]
    df = pd.DataFrame(columns=["Username", "Password", "Similarity", "Time"])

    if r is not None:
        if r.status_code == 200:
            dictionary_content = r.text
            english_dictionary = list(dictionary_content.split('\r\n'))
            for password, salt, username in database:
                start = time.time()
                res = dictionary_attack_hash(password, salt, english_dictionary)
                finish = time.time()
                df.loc[len(df)] = [username, res[0], res[1], finish-start]
        else:
            print("some other error with request")
    else:
        print("Failure loading dictionary")

    df.to_excel("dictionary_attack.xlsx", index=False)


# problem with pyCharm clipboard not synchronising with windows one
# https://stackoverflow.com/questions/31284260/how-to-sync-intellij-idea-clipboard-with-the-windows-clipboard
# Did not expect that can happen

# Salting good explanation
# https://www.youtube.com/watch?v=qgpsIBLvrGY
# https://www.youtube.com/watch?v=--tnZMuoK3E&list=LL&index=2
