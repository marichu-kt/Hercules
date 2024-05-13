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
            if mensaje.startswith("ASTAR:"):
                grafo, inicio, objetivo = crear_grafo_desde_mensaje(mensaje)
                resultado = a_star(grafo, inicio, objetivo)
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
    objetivo = int(mensaje.split(":")[2])
    return grafo, inicio, objetivo

# Función para el algoritmo A*
def a_star(grafo, inicio, objetivo):
    def heuristica(nodo):
        # En este ejemplo, simplemente devuelve la distancia entre el nodo y el objetivo
        return abs(nodo - objetivo)

    heap = [(0, inicio)]
    visitados = set()
    padres = {}

    while heap:
        costo, nodo = heapq.heappop(heap)
        if nodo == objetivo:
            # Construye el camino desde el nodo objetivo hasta el nodo inicial
            camino = []
            while nodo in padres:
                camino.append(str(nodo))
                nodo = padres[nodo]
            camino.append(str(inicio))
            return ",".join(camino[::-1])
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino, peso in grafo[nodo].items():
                costo_total = costo + peso
                heapq.heappush(heap, (costo_total + heuristica(vecino), vecino))
                if vecino not in padres or costo_total < padres[vecino]:
                    padres[vecino] = nodo

    return "No se encontró un camino"

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
