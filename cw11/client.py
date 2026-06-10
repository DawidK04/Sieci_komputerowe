import socket
import select
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def run_client():
    nickname = input("Podaj swój nickname: ").strip()
    if not nickname:
        print("Nickname nie może być pusty!")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    client_socket.setblocking(False)
    server_addr = (SERVER_HOST, SERVER_PORT)

    client_socket.sendto(b'\x00' + nickname.encode('utf-8'), server_addr)
    print("Połączono z serwerem. Możesz zacząć pisać (wpisz '/quit' aby wyjść).")

    try:
        while True:
            ready_to_read, _, _ = select.select([client_socket, sys.stdin], [], [])

            for ready in ready_to_read:
                if ready == client_socket:
                    data, _ = client_socket.recvfrom(1024)
                    print(data.decode('utf-8'))

                elif ready == sys.stdin:
                    msg = sys.stdin.readline().strip()

                    if msg == '/quit':
                        client_socket.sendto(b'', server_addr)
                        return

                    if msg:
                        client_socket.sendto(b'\x01' + msg.encode('utf-8'), server_addr)

    except KeyboardInterrupt:
        client_socket.sendto(b'', server_addr)
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()