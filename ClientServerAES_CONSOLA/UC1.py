import socket
import threading
import time

# FUNCIÓN PARA MANEJAR LA COMUNICACIÓN CON UN CLIENTE ESPECÍFICO
def manejar_cliente(cliente, direccion):
    print(f"Conexión establecida con {direccion}")

    while True:
        try:
            datos = cliente.recv(1024)
            if not datos:
                break
            mensaje = datos.decode()
            print(f"\nCliente {direccion}: {mensaje}")
        except ConnectionResetError:
            print(f"\nCliente {direccion} desconectado")
            break

    cliente.close()

# FUNCIÓN PARA ENVIAR MENSAJES DESDE EL SERVIDOR A UN CLIENTE ESPECÍFICO
def enviar_mensaje(cliente):
    while True:
        try:
            mensaje = input("Servidor: ")
            cliente.send(mensaje.encode())
        except ConnectionResetError:
            print("Error de conexión. Intentando reconectar...")
            cliente.close()
            time.sleep(1)
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            intentar_conectar(cliente)
            continue

# FUNCIÓN PARA INTENTAR CONECTAR EL CLIENTE AL SERVIDOR
def intentar_conectar(cliente):
    while True:
        try:
            cliente.connect(('127.0.0.1', 8080))
            break
        except ConnectionRefusedError:
            print("No se pudo establecer conexión. Reintentando ...")
            time.sleep(1)

# FUNCIÓN PRINCIPAL DEL PROGRAMA
def main():
    while True:
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.bind(('127.0.0.1', 8081))
            servidor.listen()    

            print("Esperando conexiones...")

            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            intentar_conectar(cliente)

            cliente_thread = threading.Thread(target=enviar_mensaje, args=(cliente,))
            cliente_thread.start()

            while True:
                cliente, direccion = servidor.accept()
                cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
                cliente_thread.start()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            servidor.close()
            cliente.close()

if __name__ == "__main__":
    main()
