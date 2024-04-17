# możliwość dodania użytkownika
# przechowuje bazę danych funkcji skrótu
# gdy server otrzymuje próbę logowania porównuje przesłany skrót do tego z bazy danych

# import hashlib
import socket
import pandas as pd
import os.path

# Constants
DATABASE_FILENAME = "user_credentials.csv"
SERVER_HOST = 'localhost'
SERVER_PORT = 12345


def generate_database():
    if not os.path.isfile(DATABASE_FILENAME):
        df = pd.DataFrame(columns=["Username", "Password"])
        df.to_csv(DATABASE_FILENAME, index=False)


def check_credentials(username, encrypted_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        if not user.empty and user.iloc[0]["Password"] == encrypted_password:
            return "Login successful."
    return "Invalid credentials."


def register_user(username, encrypted_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty and username in df["Username"].values:
        return "Username already exists."
    # df = df.append({"Username": username, "Password": encrypted_password}, ignore_index=True)
    df.loc[len(df)] = [username, encrypted_password]
    df.to_csv(DATABASE_FILENAME, index=False)
    return "Registration successful."


def change_password(username, old_password, new_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        if not user.empty and user.iloc[0]["Password"] == old_password:
            df.loc[df["Username"] == username, "Password"] = new_password
            df.to_csv(DATABASE_FILENAME, index=False)
            return "Password changed successfully."
    return "Failed to change password. Invalid username or old password."


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
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Received data: {data}")
                parts = data.split("|")
                if parts[0] == "LOGIN":
                    response = check_credentials(parts[1], parts[2])
                elif parts[0] == "REGISTER":
                    response = register_user(parts[1], parts[2])
                else:
                    response = "Invalid request."
                conn.sendall(response.encode())
