# TO DO:
#
# 2.
#    Przeprowadź testy uwierzytelniania, demonstrując, że prawidłowe hasła pozwalają na dostęp,
#    a nieprawidłowe są odrzucane. Wykaż, że serwer nie jest w stanie odtworzyć oryginalnego hasła z jego skrótu.

import pandas as pd

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



# Podpunkt 2.
# jak przeprowadzić testy uwierzytelniania? Zrobiłem to by zobaczyć czy działa i działa
# w tym pliku(main) będziemy:
# Wykaż, że serwer nie jest w stanie odtworzyć oryginalnego hasła z jego skrótu.
# Important.
#    Rozwiązanie umieść w repozytorium. Czasy eksperymentu umieść na wykresie (w arkuszu kalkulacyjnym).
#    (wpisać czasy i number próby do arkusza kalkulacyjnego i w nim robię wykres i exportuję do repo)


# problem with pyCharm clipboard not synchronising with windows one
# https://stackoverflow.com/questions/31284260/how-to-sync-intellij-idea-clipboard-with-the-windows-clipboard
# Did not expect that can happen

# Salting good explanation
# https://www.youtube.com/watch?v=qgpsIBLvrGY
# https://www.youtube.com/watch?v=--tnZMuoK3E&list=LL&index=2
