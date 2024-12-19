# Comunicación Segura con RSA y Sockets

## ¿Qué es este código?

Este código implementa un sistema de comunicación segura entre un cliente y un servidor utilizando cifrado RSA para proteger los mensajes transmitidos. A continuación, se describen los componentes principales del código:

### 1. Generación de Claves RSA

El código incluye un script para generar un par de claves RSA (pública y privada). Estas claves son necesarias para cifrar y descifrar los mensajes.

- **Clave Pública**: Utilizada por el cliente para cifrar mensajes que serán enviados al servidor.
- **Clave Privada**: Utilizada por el servidor para descifrar los mensajes recibidos del cliente.

### 2. Servidor

El servidor está diseñado para realizar las siguientes acciones:

- Escuchar conexiones entrantes de clientes.
- Recibir mensajes cifrados del cliente.
- Descifrar estos mensajes utilizando la clave privada.
- Mostrar el contenido de los mensajes en texto claro.

### 3. Cliente

El cliente realiza las siguientes acciones:

- Se conecta al servidor especificado.
- Cifra los mensajes utilizando la clave pública del servidor.
- Envía estos mensajes cifrados al servidor.

### 4. Cifrado y Descifrado

El cifrado RSA se utiliza para asegurar que los mensajes no puedan ser leídos por terceros. El cliente cifra los mensajes antes de enviarlos, y el servidor los descifra una vez que los recibe.
