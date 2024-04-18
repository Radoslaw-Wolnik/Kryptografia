# możliwość dodania użytkownika
# przechowuje bazę danych funkcji skrótu
# gdy server otrzymuje próbę logowania sprawdza czy login jest w bazie danych, jesli jest wysyla sol,
# następnie odbiera hashed password+salt i porownuje do stored hashed password

import socket
import pandas as pd
import os.path


# Constants
DATABASE_FILENAME = "user_credentials.csv"
SERVER_HOST = 'localhost'
SERVER_PORT = 12345


def generate_database():
    if not os.path.isfile(DATABASE_FILENAME):
        df = pd.DataFrame(columns=["Username", "Salt", "Password"])
        df.to_csv(DATABASE_FILENAME, index=False)


def check_credentials(username):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        if not user.empty:
            salt = user.iloc[0]["Salt"]
            return True, salt
    return False, None


def verify_login(username, hashed_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        stored_hashed_password = user.iloc[0]["Password"]
        # Compare hashed passwords
        if hashed_password == stored_hashed_password:
            return "Login successful."
    return "Invalid credentials."


def register_user(username, salt, hashed_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty and username in df["Username"].values:
        return "Username already exists."
    # Add new user to the DataFrame
    # new_user = {"Username": username, "Salt": salt, "Password": hashed_password}
    # df = df.append(new_user, ignore_index=True)
    df.loc[len(df)] = [username, salt, hashed_password]
    df.to_csv(DATABASE_FILENAME, index=False)
    return "Registration successful."


# Main server code
if __name__ == "__main__":
    generate_database()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()

        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected to {addr}")
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received data: {data}")
                    parts = data.split("|")
                    if parts[0] == "LOGIN":
                        exists, salt = check_credentials(parts[1])
                        if exists:
                            conn.sendall(b"OK")
                            conn.sendall(salt.encode())
                            password = conn.recv(1024).decode()
                            print(f"In login received: {password}")
                            response = verify_login(parts[1], password)
                            conn.sendall(response.encode())
                        else:
                            conn.sendall(b"NOT_FOUND")
                    elif parts[0] == "REGISTER":
                        data = conn.recv(1024).decode()
                        print(f"In register received: {data}")
                        parts = data.split("|")
                        response = register_user(parts[0], parts[1], parts[2])
                        conn.sendall(response.encode())
                    else:
                        conn.sendall("Invalid request.".encode())
