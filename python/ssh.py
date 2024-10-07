import socket
import paramiko
import threading

# Host key setup (you can generate one using ssh-keygen or manually)
host_key = paramiko.RSAKey.generate(2048)

# Custom server class based on paramiko.ServerInterface
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        super(SSHServer, self).__init__()

    def check_auth_password(self, username, password):
        # Automatically allow all password attempts
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        # Accept any request for a session channel
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # Accept PTY requests to prevent the error
        return True

    def check_channel_shell_request(self, channel):
        # Accept shell requests
        return True

def handle_connection(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)

    server = SSHServer()
    try:
        transport.start_server(server=server)

        # Wait for a client channel to be opened
        channel = transport.accept(20)
        if channel is not None:
            print("Client connected!")

            # Send a prompt to the client
            channel.send("What's your name? ")

            # Receive the input from the user
            user_input = receive_full_input(channel)

            # Print the received input on the server console
            print(f"Received input from client: {user_input}")

            # Respond to the client and close the connection
            channel.send(f"Hello, {user_input}!\n")
            channel.close()

    except Exception as e:
        print(f"SSH negotiation failed: {str(e)}")
    finally:
        transport.close()

def receive_full_input(channel):
    # Collect input until we receive a newline character
    data = ""
    while True:
        chunk = channel.recv(1024).decode("utf-8")
        data += chunk
        if '\n' in chunk:  # Stop once we get the full line (user presses Enter)
            break
    return data.strip()

def start_ssh_server(host="0.0.0.0", port=2222):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)
    print(f"Listening for connections on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_connection, args=(client_socket,)).start()

if __name__ == "__main__":
    start_ssh_server()
