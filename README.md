# Hercules SETUP Utility 🚀

Hercules SETUP Utility es una potente herramienta de configuración de puerto serie (RS-232 o RS-485), cliente/servidor TCP/IP y puerto virtual USB. Desarrollado por HW group, ofrece una solución integral para configurar y probar dispositivos de comunicación serie, equipos de red y puertos virtuales USB. Ya sea que seas un desarrollador, ingeniero o entusiasta, Hercules SETUP Utility proporciona una interfaz intuitiva para administrar diversos dispositivos de comunicación de manera eficiente.

![Hercules](/Images/icon.jpg)

## Características principales 🎯

- Terminal de Puerto Serie: Permite la comunicación con dispositivos serie (RS-232 o RS-485), con opciones de configuración flexibles.
- Cliente/Servidor TCP/IP: Simula roles de cliente y servidor para probar dispositivos de red como routers y servidores.
- Puerto Virtual USB: Facilita la prueba y configuración de dispositivos USB simulando puertos serie físicos.
- Registro de Datos: Ofrece capacidades de registro para análisis y depuración.
- Automatización: Permite la creación de scripts para automatizar tareas y pruebas.
- Soporte Multiidioma: Disponible en varios idiomas para una experiencia global.

## Instalación 🛠️

Para instalar PuTTY, sigue estos pasos:

1. Descarga el instalador adecuado para tu sistema operativo desde el sitio web oficial de Hercules: [hw-group.com/]([https://www.hw-group.com/software/hercules-setup-utility]).
2. Conecta tus dispositivos y configura los puertos según tus necesidades.
3. Utiliza la interfaz para probar la comunicación y realizar tareas de configuración avanzadas.

## Uso 🖥️

Para utilizar Hercules, simplemente sigue estos pasos:

1. Abre Hercules SETUP Utility desde el menú de inicio o el escritorio.
2. Elige el tipo de interfaz de comunicación que deseas configurar.
3. Ajusta la configuración del puerto según las especificaciones de tus dispositivos.
4. Establece la comunicación con tus dispositivos y realiza pruebas.
5. Explora características como registro de datos y automatización mediante scripts.
6. Consulta la documentación y busca soporte si es necesario.
7. Cierra Hercules SETUP Utility al finalizar tus tareas.

## Servidor de escucha

Hoy exploré cómo crear un servidor en Python utilizando el módulo `socket`, con el objetivo de escuchar y mostrar datos enviados por el programa Hercules. Comencé escribiendo código para manejar conexiones de clientes, luego configuré el servidor para aceptar conexiones entrantes. Después de ejecutar la aplicación y conectar Hercules al servidor, pude enviar datos y observar cómo se mostraban en la consola del servidor. Este ejercicio me permitió aprender sobre el manejo de conexiones de red en Python y cómo interactuar con programas externos a través de sockets.

1. Abre el programa Hércules en tu computadora.
2. En la pestaña "Serial", configura la configuración del puerto serie según sea necesario.
3. En la pestaña "TCP Client", ingresa la dirección IP y el puerto del servidor Python.
4. Haz clic en el botón "Connect" para conectarte al servidor Python.
5. Después de conectar, puedes escribir datos en el campo de entrada y enviarlos al servidor haciendo clic en "Send".
6. En la consola donde estés ejecutando el servidor Python, verás los mensajes que indican la recepción de datos del cliente Hércules.
7. En Hércules, puedes desconectar el cliente haciendo clic en el botón "Disconnect".

El programa de escucha en Python es: [Server](Server.py)

![Conexion](/Images/img-1.png)



