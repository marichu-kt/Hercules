import threading
import time

# Función que será ejecutada por los hilos
def imprimir_mensaje(mensaje):
    for _ in range(5):
        print(mensaje)
        time.sleep(1)  # Esperar un segundo entre cada impresión

# Crear los hilos
hilo1 = threading.Thread(target=imprimir_mensaje, args=("Hola desde el Hilo 1",))
hilo2 = threading.Thread(target=imprimir_mensaje, args=("Hola desde el Hilo 2",))

# Iniciar los hilos
hilo1.start()
hilo2.start()

# Esperar a que los hilos terminen
hilo1.join()
hilo2.join()

print("Los hilos han terminado.")
