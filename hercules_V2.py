import socket
import threading

def handle_client(client_socket, address):
    print(f"[INFO] Conexión establecida desde: {address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"[INFO] Cliente {address} desconectado.")
                break
            print(f"[INFO] Datos recibidos de {address}: {data.decode('utf-8')}")
            # Aquí puedes agregar lógica para procesar los datos recibidos
            # y enviar respuestas adecuadas al cliente.
    except Exception as e:
        print(f"[ERROR] Error en la conexión con {address}: {e}")
    finally:
        client_socket.close()

def main():
    IP = '127.0.0.1'  # Dirección IP local
    PORT = 23

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[INFO] Servidor escuchando en {IP}:{PORT}...")

    try:
        while True:
            client_socket, address = server.accept()
            # Aquí puedes agregar lógica para realizar la autenticación del cliente antes de manejar la conexión.
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()

    except KeyboardInterrupt:
        print("[INFO] Servidor detenido.")
    except Exception as e:
        print(f"[ERROR] Error en el servidor: {e}")

if __name__ == "__main__":
    main()
