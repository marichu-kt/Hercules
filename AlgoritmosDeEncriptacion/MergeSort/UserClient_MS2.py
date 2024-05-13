import socket
import threading
import time

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
            if mensaje.startswith("MSORT:"):
                numeros = [int(x) for x in mensaje.split(":")[1].split(",")]
                sorted_nums = merge_sort(numeros)
                cliente.send(str(sorted_nums).encode())
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

# Función para ordenar una lista usando MergeSort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    # Dividir la lista en mitades
    medio = len(arr) // 2
    izquierda = arr[:medio]
    derecha = arr[medio:]
    # Llamar recursivamente a merge_sort para cada mitad
    izquierda = merge_sort(izquierda)
    derecha = merge_sort(derecha)
    # Fusionar las dos mitades ordenadas
    return merge(izquierda, derecha)

# Función para fusionar dos listas ordenadas
def merge(izquierda, derecha):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    # Agregar los elementos restantes de izquierda y derecha
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

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
