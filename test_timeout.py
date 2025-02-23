import socket
import time

host = "localhost"
port = 3307  # Špatný port, aby se testovalo připojení
timeout = 1  # Timeout na 1 sekundu

start_time = time.time()
try:
    print(f"Testuji timeout {timeout} sekund...")
    sock = socket.create_connection((host, port), timeout=timeout)
except Exception as e:
    print("Chyba připojení:", e)
finally:
    elapsed_time = time.time() - start_time
    print(f"Timeout trval {elapsed_time:.2f} sekund")
