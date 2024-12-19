from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import time

# CLAVE AES COMPARTIDA ENTRE CLIENTE Y SERVIDOR
aes_key = b'SharedKeyForAES!' 

def cifrar_mensaje(mensaje):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    cifrado = cipher.encrypt(pad(mensaje.encode(), AES.block_size))
    return cipher.iv + cifrado

def descifrar_mensaje(datos):
    iv = datos[:16]
    cifrado = datos[16:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    mensaje = unpad(cipher.decrypt(cifrado), AES.block_size)
    return mensaje.decode()

def manejar_cliente(cliente, direccion):
    print(f"Conexión establecida con {direccion}")
    while True:
        try:
            datos = cliente.recv(1024)
            if not datos:
                raise ConnectionResetError("El cliente se desconectó.")
            mensaje = descifrar_mensaje(datos)
            print(f"\nServidor {direccion}: {mensaje}")
        except (socket.error, ConnectionResetError) as e:
            print(f"Error al manejar mensaje de {direccion}: {e}")
            break
    cliente.close()

def enviar_mensaje(cliente):
    while True:
        try:
            while True:
                mensaje = input("Cliente: ")
                cliente.send(cifrar_mensaje(mensaje))
        except (socket.error, ConnectionResetError):
            print("Conexión perdida. Intentando reconectar...")
            cliente.close()
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            intentar_conectar(cliente)

def intentar_conectar(cliente):
    while True:
        try:
            cliente.connect(('127.0.0.1', 8081))  
            print("Conexión establecida con UC1.")
            break
        except ConnectionRefusedError:
            print("No se pudo establecer conexión con UC1. Reintentando...")
            time.sleep(1)

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('127.0.0.1', 8080)) 
    servidor.listen()

    print("Esperando conexiones...")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intentar_conectar(cliente)  

    threading.Thread(target=enviar_mensaje, args=(cliente,)).start()

    while True:
        try:
            conn, direccion = servidor.accept()
            threading.Thread(target=manejar_cliente, args=(conn, direccion)).start()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
