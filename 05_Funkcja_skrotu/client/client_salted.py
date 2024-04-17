import socket
import hashlib
import os
import secrets

def login(client_socket, username, password):
    try:
        # Send login signal to the server
        client_socket.send(b"LOGIN")

        # Receive salt from the server
        salt_hex = client_socket.recv(1024).decode()
        salt = bytes.fromhex(salt_hex)

        # Generate a hash of the password with the received salt
        hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

        # Send username and hashed password to the server
        message = f"{username}|{hashed_password}"
        client_socket.send(message.encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        print(response)  # Print server response
        return response == "Login successful."

    except Exception as e:
        print(f"Error: {e}")
        return False

def register(client_socket, username, password):
    try:
        # Generate a random salt
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
        print(response)  # Print server response
        return response == "Registration successful."

    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Establish connection with the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))  # Connect to the server

        while True:
            choice = input("Choose an option:\n1. Login\n2. Register\n3. Exit\n")
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                if login(client_socket, username, password):
                    # Continue session after successful login
                    # Add your session logic here
                    pass
                else:
                    print("Login failed. Please try again.")
            elif choice == "2":
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                if register(client_socket, username, password):
                    print("Registration successful. You can now login.")
                else:
                    print("Registration failed. Please try again.")
            elif choice == "3":
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    main()
