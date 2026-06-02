import socket
import threading

# This list will store all the active client sockets so we can loop through them
clients = []

# This function sends a message to EVERYONE connected except the person who sent it


def broadcast(message_bytes, sender_socket):
    print(
        f"\n[DEBUG] Broadcast triggered. Total active clients in list: {len(clients)}")
    print("----------------------------------------------------------------")

    for client in clients:
        try:
            client.send(message_bytes)
        except:
            # If a client socket is broken/dead, remove it safely
            if client in clients:
                clients.remove(client)

# This is the function our worker threads will run independently


def handle_client(client_socket, client_address):

    while True:
        try:
            received_bytes = client_socket.recv(1024)
            if not received_bytes:
                print(
                    f"\n[System] Client {client_address} disconnected smoothly.")
                break

            # OLD: received_message = received_bytes.decode('utf-8')
            # OLD: print(f"[{client_address}] says: {received_message}")

            # Decode the message on the server just for the terminal logs
            incoming_text = received_bytes.decode('utf-8')

            # Print exactly who said what, and show current active user count
            print(
                f"\n[CHAT LOG] {incoming_text} | (Active Users: {len(clients)})")

            # Send the received message to ALL other clients
            broadcast(received_bytes, client_socket)

        except:
            # If something goes wrong (like a forced crash), catch the error
            print(f"\n[System] Client {client_address} encountered an error.")
            break

    # close this specific client's socket
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()


# AF_INET means we are using IPv4 (standard IP addresses)
# SOCK_STREAM means we are using TCP (reliable connection, perfect for chat)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# '127.0.0.1' is 'localhost' (it means this exact computer)
# 55555 is a random high port number that isn't being used by other apps
HOST = '127.0.0.1'
PORT = 55555

# Bind the socket to our host and port (Plugging the phone into the wall)
server.bind((HOST, PORT))

# Put the server into listening mode
server.listen()
print(f"Server is running and listening on {HOST}:{PORT}...")

while True:
    # This line blocks and pauses your program, waiting for a client to connect
    client_socket, client_address = server.accept()

    # Once someone connects, the code resumes and prints this:
    print(f"\n[System] Connection established with {client_address}!")

    # Save the new client to our global list before starting their thread
    clients.append(client_socket)

    # Create a new thread (worker) dedicated to this client
    # target = the function to run, args = the variables to pass to that function
    new_thread = threading.Thread(
        target=handle_client, args=(client_socket, client_address))

    # Start the thread running in the background
    new_thread.start()
