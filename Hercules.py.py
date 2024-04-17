import socket
import threading

def recibir_mensajes(client_socket):
    while True:
        try:
            mensaje_recibido = client_socket.recv(1024).decode()
            print("Mensaje recibido:", mensaje_recibido)
        except Exception as e:
            print("Error al recibir mensaje:", e)
            break

def enviar_mensaje(client_socket):
    while True:
        mensaje_enviar = input("Ingrese un mensaje: ")
        try:
            client_socket.send(mensaje_enviar.encode())
        except Exception as e:
            print("Error al enviar mensaje:", e)
            break

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Esperando conexiones...")
    client1_socket, client1_address = server_socket.accept()
    print("Cliente 1 conectado:", client1_address)
    client2_socket, client2_address = server_socket.accept()
    print("Cliente 2 conectado:", client2_address)

    thread_recibir_1 = threading.Thread(target=recibir_mensajes, args=(client1_socket,))
    thread_enviar_1 = threading.Thread(target=enviar_mensaje, args=(client1_socket,))
    thread_recibir_2 = threading.Thread(target=recibir_mensajes, args=(client2_socket,))
    thread_enviar_2 = threading.Thread(target=enviar_mensaje, args=(client2_socket,))

    thread_recibir_1.start()
    thread_enviar_1.start()
    thread_recibir_2.start()
    thread_enviar_2.start()

    # No se llama a join() para permitir que los hilos se ejecuten simultáneamente

    # client1_socket.close()
    # client2_socket.close()
    # server_socket.close()

if __name__ == "__main__":
    main()
