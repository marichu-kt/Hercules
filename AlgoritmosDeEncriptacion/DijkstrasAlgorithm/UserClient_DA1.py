import socket
import threading
import time
import heapq

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
            if mensaje.startswith("DIJKSTRA:"):
                grafo, inicio = crear_grafo_desde_mensaje(mensaje)
                resultado = dijkstra(grafo, inicio)
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
            cliente.connect(('127.0.0.1', 8080))  # Puerto y IP del cliente
            break
        except ConnectionRefusedError:
            print("No se pudo establecer conexión. Reintentando ...")
            time.sleep(1)

# Función para crear un grafo a partir del mensaje recibido del cliente
def crear_grafo_desde_mensaje(mensaje):
    lineas = mensaje.split("\n")[1:]
    grafo = {}
    for linea in lineas:
        nodo, adyacentes = linea.split(":")
        adyacentes = [x.split(",") for x in adyacentes.split(";")]
        adyacentes = {int(x[0]): int(x[1]) for x in adyacentes if x[0] and x[1]}
        grafo[int(nodo)] = adyacentes
    inicio = int(mensaje.split(":")[1].split(";")[0])
    return grafo, inicio

# Función para el algoritmo de Dijkstra
def dijkstra(grafo, inicio):
    distancia = {nodo: float('inf') for nodo in grafo}
    distancia[inicio] = 0
    heap = [(0, inicio)]

    while heap:
        costo, nodo = heapq.heappop(heap)
        if costo > distancia[nodo]:
            continue
        for vecino, peso in grafo[nodo].items():
            costo_total = costo + peso
            if costo_total < distancia[vecino]:
                distancia[vecino] = costo_total
                heapq.heappush(heap, (costo_total, vecino))

    resultado = {nodo: distancia[nodo] if distancia[nodo] != float('inf') else "inf" for nodo in grafo}
    return ",".join(f"{nodo}:{distancia}" for nodo, distancia in resultado.items())

# Función principal del programa
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
