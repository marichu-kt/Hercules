import socket

def send_data_to_hercules():
    target_ip = "127.0.0.1"
    target_port = 23

    try:
        # Crea un socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta al servidor Hercules
        client_socket.connect((target_ip, target_port))

        while True:
            # Obtiene los datos a enviar
            data = input("Ingrese los datos a enviar a Hercules ('salir' para finalizar): ")

            # Envía los datos al servidor
            client_socket.send(data.encode())

            # Verifica si se debe salir del bucle
            if data.lower() == "salir":
                break

            # Recibe la respuesta del servidor
            response = client_socket.recv(1024).decode()
            print("Respuesta del servidor: " + response)

        # Cierra la conexión
        client_socket.close()

    except ConnectionRefusedError:
        print("No se pudo establecer una conexión con el servidor Hercules.")

# Llama a la función para enviar los datos
send_data_to_hercules()