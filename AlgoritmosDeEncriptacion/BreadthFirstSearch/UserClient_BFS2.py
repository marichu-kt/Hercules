import socket
import threading
import time
from collections import deque

# Función para manejar la comunicación con un cliente específico
def manejar_cliente(cliente, direccion):
    print(f"Conexión establecida con {direccion}")

    while True:
        try:
            datos = cliente.recv(1024)
            if not datos:
                break
            mensaje = datos.decode()
            print(f"\nCliente {direccion}: {mensaje}")
            if mensaje.startswith("BFS:"):
                grafo = crear_grafo_desde_mensaje(mensaje)
                inicio = int(mensaje.split(":")[1])
                resultado = bfs(grafo, inicio)
                cliente.send(resultado.encode())
        except ConnectionResetError:
            print(f"\nCliente {direccion} desconectado")
            break

    cliente.close()

# Función para enviar mensajes desde el servidor a un cliente específico
def enviar_mensaje(cliente):
    while True:
        try:
            mensaje = input("Servidor: ")
            cliente.send(mensaje.encode())
        except ConnectionResetError:
            print("Error de conexión. Intentando reconectar...")
            cliente.close()  # Cerrar el socket
            time.sleep(1)
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Volver a abrir el socket
            intentar_conectar(cliente)
            continue  # Continuar el bucle para volver a intentar enviar mensajes

# Función para intentar conectar el cliente al servidor
def intentar_conectar(cliente):
    while True:
        try:
            cliente.connect(('127.0.0.1', 8081))  # Puerto y IP del cliente
            break
        except ConnectionRefusedError:
            print("No se pudo establecer conexión. Reintentando ...")
            time.sleep(1)

# Función para crear un grafo a partir del mensaje recibido del cliente
def crear_grafo_desde_mensaje(mensaje):
    lineas = mensaje.split("\n")[1:]
    grafo = {}
    for linea in lineas:
        nodo, vecinos = linea.split(":")
        vecinos = [int(x) for x in vecinos.split(",") if x != ""]
        grafo[int(nodo)] = vecinos
    return grafo

# Función para el algoritmo de Búsqueda en Amplitud (BFS)
def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    resultado = []

    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            resultado.append(str(nodo))
            for vecino in grafo[nodo]:
                if vecino not in visitados:
                    cola.append(vecino)

    return ",".join(resultado)

# Función principal del programa
def main():
    while True:
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.bind(('127.0.0.1', 8080))
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
