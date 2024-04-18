# ma możliwość utworzenia nowego konta
# przy logowaniu przesyła hasło zmienione za pomocą funkcji skrótu

import socket
import hashlib


def login(username, password):
    try:
        # Encrypt the password before sending it to the server
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))  # Connect to the server

            # Send username and encrypted password to the server
            message = f"LOGIN|{username}|{encrypted_password}"
            client_socket.send(message.encode())

            # Receive response from the server
            response = client_socket.recv(1024).decode()
            print(response)  # Print server response

    except Exception as e:
        print(f"Error: {e}")


def register(username, password):
    try:
        # Encrypt the password before sending it to the server
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))  # Connect to the server

            # Send username and encrypted password to the server
            message = f"REGISTER|{username}|{encrypted_password}"
            client_socket.send(message.encode())

            # Receive response from the server
            response = client_socket.recv(1024).decode()
            print(response)  # Print server response

    except Exception as e:
        print(f"Error: {e}")


# Main code to interact with the user
if __name__ == "__main__":
    while True:
        choice = input("Choose an option:\n1. Login\n2. Register\n3. Exit\n")
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == "2":
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            register(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

