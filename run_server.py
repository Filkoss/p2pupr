import socket
import threading
import config
from bank import Bank
from bank_server import handle_client

def get_ip_address():
    try:
        # Vytvoří socket a připojí se na externí server, aby zjistil veřejnou IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_server():
    ip_address = get_ip_address()
    bank = Bank(ip_address)

    print(f"[START] Server naslouchá na {config.HOST}:{config.PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.HOST, config.PORT))
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, bank))
        thread.start()

if __name__ == "__main__":
    start_server()
