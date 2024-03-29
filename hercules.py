import socket
import threading

def handle_client(client_socket, address):
    print(f"[INFO] Conexión establecida desde: {address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            print(f"[INFO] Cliente {address} desconectado.")
            break
        print(f"[INFO] Datos recibidos de {address}: {data.decode('utf-8')}")

    client_socket.close()

def main():
    IP = '127.0.0.1'  # Cambia la dirección IP a '0.0.0.0'
    PORT = 23

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[INFO] Servidor escuchando en {IP}:{PORT}...")

    try:
        while True:
            client_socket, address = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()

    except KeyboardInterrupt:
        print("[INFO] Servidor detenido.")

if __name__ == "__main__":
    main()
