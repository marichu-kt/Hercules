import socket
import threading

def enviar_mensaje(servidor_socket):
    while True:
        mensaje = input("Servidor: ")
        servidor_socket.send(mensaje.encode())

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('127.0.0.1', 23))
    servidor.listen()

    cliente, direccion = servidor.accept()
    print(f"Conexión establecida con {direccion}")

    hilo_envio = threading.Thread(target=enviar_mensaje, args=(cliente,))
    hilo_envio.start()

    while True:
        datos = cliente.recv(1024)
        print("Cliente:", datos.decode())

if __name__ == "__main__":
    main()