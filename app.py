import socket
import threading
import os
import sys

import client

# --- UI COLORS (ANSI ESCAPE CODES) ---
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================
#                      CLIENT USER INTERFACE
# ============================================================

def client_receive_worker(client_socket, username):
    while True:
        try:
            received_bytes = client_socket.recv(1024)
            if not received_bytes:
                print(f"\n{RED}[System] Server closed connection.{RESET}")
                break
            
            message = received_bytes.decode('utf-8')
            
            # --- DUPLICATION FILTER ---
            # If the message starts with your own username prefix, drop it
            if message.startswith(f"{GREEN}{BOLD}{username}{RESET}") or message.startswith(f"{CYAN}{BOLD}{username}{RESET}"):
                continue
            
            # --- COLORFUL PEER NAMES ---
            # If the incoming message is a link share, keep it Cyan.
            # Otherwise, force incoming messages from your partner to show up in vibrant MAGENTA.
            if "🔗 LINK SHARE:" not in message:
                # Find where the name colon ends and swap the color code to MAGENTA
                if ":" in message:
                    name_part, text_part = message.split(":", 1)
                    # Strip out old green color codes and apply Magenta to the partner's name
                    clean_name = name_part.replace(GREEN, "").replace(BOLD, "").replace(RESET, "").strip()
                    message = f"{MAGENTA}{BOLD}{clean_name}{RESET}:{text_part}"

            # Print the incoming message cleanly
            print(f"\n{message}")
        except:
            print(f"\n{RED}[System] Lost connection to server.{RESET}")
            break
    client_socket.close()
    os._exit(0)

def run_client_engine():
    clear_screen()
    print(f"{CYAN}============================================================{RESET}")
    print(f"{CYAN}{BOLD}🔌 CONNECT TO A CHATROOM{RESET}")
    print(f"{CYAN}============================================================{RESET}")
    
    server_ip = input("👉 Enter Server IP: ").strip()
    username = input("👉 Enter your Chat Username: ").strip()
    
    if not server_ip or not username:
        print(f"{RED}[Error] IP and Username cannot be empty!{RESET}")
        input("\nPress Enter to return...")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, 55555))
    except:
        print(f"\n{RED}[System] Could not connect to {server_ip}:55555. Check if server is running!{RESET}")
        input("\nPress Enter to return to menu...")
        return

    clear_screen()
    print(f"{GREEN}============================================================{RESET}")
    print(f"{GREEN}🟢 CHATROOM ACTIVE  |  👤 User: {username}{RESET}")
    print(f"{GREEN}============================================================{RESET}")
    print(f"{YELLOW}⚡ [QUICK ACTION]: Type '/link <url>' to broadcast web links.{RESET}")
    print(f"{YELLOW}⚡ [QUICK ACTION]: Type '/quit' to leave the chatroom.{RESET}")
    print(f"------------------------------------------------------------\n")

    # Start the listening thread and pass username
    receiver = threading.Thread(target=client_receive_worker, args=(client, username))
    receiver.daemon = True
    receiver.start()

    # Main text entry loop
    while True:
        try:
            user_input = input().strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == '/quit':
                print(f"{YELLOW}[System] Exiting chatroom...{RESET}")
                break

            # Parse if it is a link share command
            if user_input.startswith('/link '):
                raw_url = user_input.replace('/link ', '', 1)
                full_message = f"{GREEN}{BOLD}{username}{RESET}: {CYAN}{UNDERLINE}🔗 LINK SHARE: {raw_url}{RESET}"
            else:
                full_message = f"{GREEN}{BOLD}{username}{RESET}: {user_input}"

            # Send out to the server pipeline
            client.send(full_message.encode('utf-8'))
            
        except (KeyboardInterrupt, SystemExit):
            break

    client.close()

# ============================================================
#                      MAIN MENU ROUTINE
# ============================================================

def main_menu():
    while True:
        clear_screen()
        print(f"{BLUE}============================================================{RESET}")
        print(f"{BLUE}{BOLD}              🌐 TERMINAL CHATROOM CLIENT 🌐{RESET}")
        print(f"{BLUE}============================================================{RESET}")
        print(f"    [{CYAN}1{RESET}] 🔌 CONNECT TO SERVER")
        print(f"    [{RED}2{RESET}] ❌ EXIT APPLICATION")
        print(f"{BLUE}============================================================{RESET}")
        
        choice = input("👉 Please select an option (1-2): ").strip()
        
        if choice == '1':
            run_client_engine()
        elif choice == '2':
            print(f"\n{YELLOW}Goodbye!{RESET}")
            break
        else:
            print(f"\n{RED}Invalid choice! Please select 1 or 2.{RESET}")
            import time
            time.sleep(1.5)

if __name__ == "__main__":
    main_menu()