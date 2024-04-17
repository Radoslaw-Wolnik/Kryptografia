import socket
import hashlib
import pandas as pd
import os.path
import secrets

# Constants
DATABASE_FILENAME = "user_credentials.csv"
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def generate_database():
    if not os.path.isfile(DATABASE_FILENAME):
        df = pd.DataFrame(columns=["Username", "Salt", "Password"])
        df.to_csv(DATABASE_FILENAME, index=False)

def hash_password(password, salt):
    salted_password = salt + password.encode()
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

def check_credentials(username, hashed_password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        if not user.empty:
            stored_salt = bytes.fromhex(user.iloc[0]["Salt"])
            stored_hashed_password = user.iloc[0]["Password"]
            # Hash the received password using the stored salt
            hashed_password_to_compare = hash_password(hashed_password, stored_salt)
            # Compare hashed passwords
            if hashed_password_to_compare == stored_hashed_password:
                return "Login successful."
    return "Invalid credentials."


def register_user(username, password):
    df = pd.read_csv(DATABASE_FILENAME)
    if not df.empty and username in df["Username"].values:
        return "Username already exists."
    # Generate a random salt
    salt = secrets.token_bytes(16)
    # Hash the password with the salt
    hashed_password = hash_password(password, salt)
    # Append the new user to the DataFrame
    new_user = {"Username": username, "Salt": salt.hex(), "Password": hashed_password}
    df = df.append(new_user, ignore_index=True)
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
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Received data: {data}")
                parts = data.split("|")
                if parts[0] == "LOGIN":
                    response = check_credentials(parts[1], parts[2], parts[3])
                elif parts[0] == "REGISTER":
                    response = register_user(parts[1], parts[2])
                else:
                    response = "Invalid request."
                conn.sendall(response.encode())
