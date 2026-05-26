import socket
import threading
import sys

# 1. Function to constantly listen for messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Wait for data coming from the server's broadcast
            received_bytes = client_socket.recv(1024)
            if not received_bytes:
                print("\n[System] Disconnected from the server.")
                break
                
            # Decode and display the message
            message = received_bytes.decode('utf-8')
            print(f"\n{message}\n")
            
        except:
            print("\n[System] An error occurred while receiving data.")
            break
            
    client_socket.close()
    sys.exit()

# 2. Function to constantly catch user typing and send it to the server
def send_messages(client_socket, username):
    while True:
        try:
            # Get input from the terminal screen
            user_input = input()
            
            # If the user types '/quit', close down smoothly
            if user_input.lower() == '/quit':
                print("[System] Quitting chat...")
                break
                
            # Format the message so everyone knows who sent it
            full_message = f"{username}: {user_input}"
            
            # Encode and send to the server
            client_socket.send(full_message.encode('utf-8'))
            
        except:
            print("[System] An error occurred while sending data.")
            break
            
    client_socket.close()
    sys.exit()

# --- Main Client Setup ---
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 55555
    
    # Pick a username for the chatroom
    username = input("Enter your username: ")
    
    try:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[System] Connected successfully to the server at {SERVER_IP}:{SERVER_PORT}!")
    except:
        print("[System] Could not connect to the server. Make sure server.py is running.")
        return

    # 🚀 SPAWN THE THREADS 🚀
    # Thread A: Dedicated entirely to listening for incoming broadcasts
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    
    # Thread B: Dedicated entirely to capturing user keystrokes and sending them
    send_thread = threading.Thread(target=send_messages, args=(client, username))
    send_thread.start()

if __name__ == "__main__":
    start_client()