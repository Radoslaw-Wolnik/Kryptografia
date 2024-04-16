import socket
import hashlib
import pandas as pd

# Constants
DATABASE_FILENAME = "user_credentials.xlsx"

def generate_database():
    if not os.path.isfile(DATABASE_FILENAME):
        df = pd.DataFrame(columns=["Username", "Password"])
        df.to_excel(DATABASE_FILENAME, index=False)

def check_credentials(username, password):
    df = pd.read_excel(DATABASE_FILENAME)
    if not df.empty:
        user = df[df["Username"] == username]
        if not user.empty and user.iloc[0]["Password"] == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False

def register_user(username, password):
    df = pd.read_excel(DATABASE_FILENAME)
    if not df.empty and username in df["Username"].values:
        return False  # Username already exists
    df = df.append({"Username": username, "Password": hashlib.sha256(password.encode()).hexdigest()}, ignore_index=True)
    df.to_excel(DATABASE_FILENAME, index=False)
    return True

# Server setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Server started. Listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            # Receive data from client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Process client request
            request = data.split("|")
            if request[0] == "LOGIN":
                username = request[1]
                password = request[2]
                if check_credentials(username, password):
                    client_socket.sendall("LOGIN_SUCCESS".encode())
                else:
                    client_socket.sendall("LOGIN_FAILED".encode())
            elif request[0] == "REGISTER":
                username = request[1]
                password = request[2]
                if register_user(username, password):
                    client_socket.sendall("REGISTER_SUCCESS".encode())
                else:
                    client_socket.sendall("REGISTER_FAILED".encode())
            else:
                client_socket.sendall("INVALID_REQUEST".encode())

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()

# Main server code
if __name__ == "__main__":
    generate_database()
    start_server()
