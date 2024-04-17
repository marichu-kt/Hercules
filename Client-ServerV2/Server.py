import socket
import threading

def enviar_mensaje(cliente_socket):
    while True:
        mensaje = input("Cliente: ")
        cliente_socket.send(mensaje.encode())

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 23))

    hilo_envio = threading.Thread(target=enviar_mensaje, args=(cliente,))
    hilo_envio.start()

    while True:
        datos = cliente.recv(1024)
        print("Servidor:", datos.decode())

if __name__ == "__main__":
    main()