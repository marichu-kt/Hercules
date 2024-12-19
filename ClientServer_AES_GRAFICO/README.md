# Comunicación Cliente-Servidor con Cifrado AES 🔒

Este proyecto implementa una comunicación cliente-servidor utilizando **AES (Advanced Encryption Standard)** en modo CBC para cifrar y descifrar mensajes enviados entre dos nodos: `UC1` (Servidor) y `UC2` (Cliente).

## Descripción 📝

El sistema consiste en dos scripts:

- **`UC1` (Servidor):**
  - Escucha conexiones entrantes desde clientes en el puerto `8081`.
  - Se conecta como cliente al `UC2` en el puerto `8080`.
  - Encripta y desencripta mensajes utilizando una clave AES compartida.

- **`UC2` (Cliente):**
  - Escucha conexiones entrantes desde el servidor en el puerto `8080`.
  - Se conecta como cliente al `UC1` en el puerto `8081`.
  - También utiliza cifrado y descifrado AES con la clave compartida.

## Características 📋

- **Cifrado AES:** 
  - La clave compartida `SharedKeyForAES!` garantiza la seguridad en la transmisión.
  - Cada mensaje se cifra utilizando una **clave de inicialización (IV)** única.

- **Reconexión Automática:**
  - Si la conexión falla, el sistema intenta reconectarse automáticamente al otro nodo.

- **Multi-threading:** 
  - Maneja múltiples conexiones simultáneas con hilos independientes.

- **Compatibilidad:** 
  - Funciona en entornos locales (`127.0.0.1`) para pruebas, pero puede configurarse para redes remotas.
