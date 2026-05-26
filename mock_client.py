
import socket
import time # Imported to allow us to pause/sleep

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
print("Successfully connected to the server!")

# Send message 1
client.send("Message 1: Hello!".encode('utf-8'))
time.sleep(2) # Pause for 2 seconds

# Send message 2
client.send("Message 2: Are you still there?".encode('utf-8'))
time.sleep(2)

# Send message 3
client.send("Message 3: Goodbye!".encode('utf-8'))
time.sleep(1)

# Clean up and close
client.close()