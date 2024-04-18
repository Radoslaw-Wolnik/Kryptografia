import socket
import hashlib
import time
import secrets
import pandas as pd
from openpyxl.workbook import Workbook


def register(client_socket, username, password):
    try:
        # Generate salt
        salt = secrets.token_bytes(16)

        # Hash the password with the salt
        hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

        # Send register signal to the server
        client_socket.send(b"REGISTER")

        # Send username, salt, and hashed password to the server
        message = f"{username}|{salt.hex()}|{hashed_password}"
        client_socket.send(message.encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        return response == "Registration successful."

    except Exception as e:
        print(f"Error: {e}")
        return False


def login(client_socket, username, password):
    try:
        # Send login request and username to the server
        client_socket.send(f"LOGIN|{username}".encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        if response != "OK":
            return False

        # Receive salt from the server and convert it to bytes
        salt_hex = client_socket.recv(1024).decode()
        salt = bytes.fromhex(salt_hex)

        # Hash the password with the salt
        hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()
        # Send hashed password to the server
        client_socket.send(hashed_password.encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        return response == "Login successful."

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    df = pd.DataFrame(columns=["Username", "Successful", "Time"])
    # Establish connection with the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))  # Connect to the server

        # Register 10 users with passwords
        users = []
        usernames = ["allicelice", "bobbyb", "charly", "david0dav", "emilyem", "frankrank", "gracee", "henryh", "isabellab", "jackjack"]
        passwords = ["sunshine", "rainbow", "butterfly", "unicorn", "moonlight", "starlight", "waterfall", "firefly", "raindrop", "ocean"]
        for i in range(len(usernames)):
            username = usernames[i]
            password = passwords[i]
            # success = register(client_socket, username, password) # first time to register users
            success = True
            if success:
                users.append((username, password))
                print(f"User {username} registered successfully.")
            else:
                print(f"Failed to register user {username}.")

        # Test authentication for registered users
        for username, password in users:
            # Test authentication with correct password
            start_time = time.time()
            success = login(client_socket, username, password)
            end_time = time.time()
            if success:
                print(f"Authentication for user {username} with correct password successful.")
            else:
                print(f"Authentication for user {username} with correct password failed.")
            print(f"Time taken for authentication with correct password: {end_time - start_time} seconds")
            # df = df.append({"Username": username, "Successful": success, "Time": end_time - start_time}, ignore_index=True)
            df.loc[len(df)] = [username, success, end_time - start_time]
            # Test authentication with incorrect password
            start_time = time.time()
            success = login(client_socket, username, "incorrect_password")
            end_time = time.time()
            if not success:
                print(f"Authentication for user {username} with incorrect password rejected.")
            else:
                print(f"Authentication for user {username} with incorrect password succeeded.")
            print(f"Time taken for authentication with incorrect password: {end_time - start_time} seconds")
            # df = df.append({"Username": username, "Successful": success, "Time": end_time - start_time}, ignore_index=True)
            df.loc[len(df)] = [username, success, end_time - start_time]

        # Save the DataFrame to an Excel file
        df.to_excel("login_attempts.xlsx", index=False)

if __name__ == "__main__":
    main()
