import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import time

# CLAVE AES COMPARTIDA ENTRE CLIENTE Y SERVIDOR
aes_key = b'SharedKeyForAES!'

def cifrar_mensaje(mensaje):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    cifrado = cipher.encrypt(pad(mensaje.encode(), AES.block_size))
    return cipher.iv + cifrado

def descifrar_mensaje(datos):
    iv = datos[:16]
    cifrado = datos[16:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    mensaje = unpad(cipher.decrypt(cifrado), AES.block_size)
    return mensaje.decode()

class ChatServidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - UC1")
        self.root.geometry("800x700")
        self.root.config(bg="#212121")
        self.root.resizable(False, False)

        # Variables de conexión
        self.servidor = None
        self.cliente = None
        self.conectado = False

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ttk.Label(self.root, text="Servidor - UC1", font=("Arial", 24, "bold"), background="#212121", foreground="#ffffff")
        self.title_label.pack(pady=10)

        # Configuración
        self.config_frame = ttk.Frame(self.root, padding=10)
        self.config_frame.pack(pady=10)

        self.server_ip_label = ttk.Label(self.config_frame, text="IP Servidor:", font=("Arial", 12))
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.server_ip_entry = ttk.Entry(self.config_frame, width=20)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.server_port_label = ttk.Label(self.config_frame, text="Puerto Servidor:", font=("Arial", 12))
        self.server_port_label.grid(row=0, column=2, padx=5, pady=5)
        self.server_port_entry = ttk.Entry(self.config_frame, width=10)
        self.server_port_entry.insert(0, "8080")
        self.server_port_entry.grid(row=0, column=3, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Detener Servidor", command=self.detener_servidor)
        self.stop_button.pack(pady=5)

        # Área de mensajes
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, bg="#2c2c2c", fg="#ffffff", font=("Arial", 12))
        self.chat_display.pack(pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Entrada de Mensaje
        self.message_entry = ttk.Entry(self.root, width=70)
        self.message_entry.pack(pady=10)

        self.send_button = ttk.Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje)
        self.send_button.pack(pady=5)

    def iniciar_servidor(self):
        ip_servidor = self.server_ip_entry.get()
        puerto_servidor = int(self.server_port_entry.get())

        try:
            self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.servidor.bind((ip_servidor, puerto_servidor))
            self.servidor.listen(5)
            self.mostrar_mensaje(f"Servidor iniciado en {ip_servidor}:{puerto_servidor}")
            self.conectado = True

            # Hilo para aceptar conexiones entrantes
            threading.Thread(target=self.aceptar_conexiones, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")

    def detener_servidor(self):
        if self.conectado:
            if self.cliente:
                self.cliente.close()
            if self.servidor:
                self.servidor.close()
            self.conectado = False
            self.mostrar_mensaje("Servidor detenido.")
        else:
            messagebox.showwarning("Advertencia", "El servidor no está activo.")

    def aceptar_conexiones(self):
        while self.conectado:
            try:
                cliente, direccion = self.servidor.accept()
                self.cliente = cliente
                self.mostrar_mensaje(f"Cliente conectado desde {direccion}")

                # Hilo para manejar mensajes del cliente
                threading.Thread(target=self.recibir_mensajes, args=(cliente,), daemon=True).start()
            except Exception:
                break

    def recibir_mensajes(self, cliente):
        while self.conectado:
            try:
                datos = cliente.recv(1024)
                if datos:
                    mensaje = descifrar_mensaje(datos)
                    self.mostrar_mensaje(f"Cliente: {mensaje}")
            except Exception:
                self.mostrar_mensaje("Conexión con el cliente perdida.")
                break

    def enviar_mensaje(self):
        if not self.cliente:
            messagebox.showwarning("Advertencia", "No hay cliente conectado.")
            return

        mensaje = self.message_entry.get()
        if not mensaje:
            messagebox.showwarning("Advertencia", "Por favor, escribe un mensaje.")
            return

        try:
            mensaje_cifrado = cifrar_mensaje(mensaje)
            self.cliente.send(mensaje_cifrado)
            self.mostrar_mensaje(f"Tú: {mensaje}")
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

    def mostrar_mensaje(self, mensaje):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, mensaje + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatServidor(root)
    root.mainloop()
