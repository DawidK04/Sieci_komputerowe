import socket

HOST = '127.0.0.1'
PORT = 12345

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    
    users = {} 
    
    print(f"Serwer nasłuchuje na {HOST}:{PORT}...")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)

            if not data:
                if addr in users:
                    print(f"[-] Użytkownik {users[addr]} rozłączył się.")
                    del users[addr]
                continue

            prefix = data[0:1]
            content = data[1:]

            if prefix == b'\x00':
                nickname = content.decode('utf-8')
                users[addr] = nickname
                print(f"[+] Nowy użytkownik: {nickname} (adres: {addr})")

            elif prefix == b'\x01':
                if addr in users:
                    nickname = users[addr]
                    message_str = content.decode('utf-8')
                    formatted_message = f"{nickname}: {message_str}".encode('utf-8')

                    for client_addr in users.keys():
                        if client_addr != addr:
                            server_socket.sendto(formatted_message, client_addr)
                else:
                    pass

        except KeyboardInterrupt:
            print("\nZamykanie serwera...")
            break
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    server_socket.close()

if __name__ == "__main__":
    run_server()
