import socket
import threading

def send_data_to_hercules():
    target_ip = "127.0.0.1"
    target_port = 23

    try:
        # Crea un socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta al servidor Hercules
        client_socket.connect((target_ip, target_port))

        # Define una función para recibir datos del servidor
        def receive_data():
            while True:
                response = client_socket.recv(1024).decode()
                if not response:
                    break
                print("Respuesta del servidor: " + response)

        # Inicia un hilo para recibir datos del servidor
        receive_thread = threading.Thread(target=receive_data)
        receive_thread.start()

        while True:
            # Obtiene los datos a enviar
            data = input("Ingrese los datos a enviar a Hercules ('salir' para finalizar): ")

            # Envía los datos al servidor
            client_socket.send(data.encode())

            # Verifica si se debe salir del bucle
            if data.lower() == "salir":
                break

        # Espera a que el hilo de recepción termine
        receive_thread.join()

        # Cierra la conexión
        client_socket.close()

    except ConnectionRefusedError:
        print("No se pudo establecer una conexión con el servidor Hercules.")

# Llama a la función para enviar los datos
send_data_to_hercules()
