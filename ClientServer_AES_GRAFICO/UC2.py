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

class ChatCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente - UC2")
        self.root.geometry("800x700")
        self.root.config(bg="#212121")
        self.root.resizable(False, False)

        # Variables de conexión
        self.cliente = None
        self.conectado = False

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ttk.Label(self.root, text="Cliente - UC2", font=("Arial", 24, "bold"), background="#212121", foreground="#ffffff")
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

        self.connect_button = ttk.Button(self.root, text="Conectar", command=self.conectar_servidor)
        self.connect_button.pack(pady=5)

        self.disconnect_button = ttk.Button(self.root, text="Desconectar", command=self.desconectar_servidor)
        self.disconnect_button.pack(pady=5)

        # Área de mensajes
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, bg="#2c2c2c", fg="#ffffff", font=("Arial", 12))
        self.chat_display.pack(pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Entrada de Mensaje
        self.message_entry = ttk.Entry(self.root, width=70)
        self.message_entry.pack(pady=10)

        self.send_button = ttk.Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje)
        self.send_button.pack(pady=5)

    def conectar_servidor(self):
        ip_servidor = self.server_ip_entry.get()
        puerto_servidor = int(self.server_port_entry.get())

        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((ip_servidor, puerto_servidor))
            self.conectado = True
            self.mostrar_mensaje(f"Conectado al servidor en {ip_servidor}:{puerto_servidor}")

            # Hilo para recibir mensajes
            threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def desconectar_servidor(self):
        if self.conectado:
            self.cliente.close()
            self.conectado = False
            self.mostrar_mensaje("Desconectado del servidor.")
        else:
            messagebox.showwarning("Advertencia", "No estás conectado a ningún servidor.")

    def enviar_mensaje(self):
        if not self.conectado:
            messagebox.showwarning("Advertencia", "No estás conectado a un servidor.")
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

    def recibir_mensajes(self):
        while self.conectado:
            try:
                datos = self.cliente.recv(1024)
                if datos:
                    mensaje = descifrar_mensaje(datos)
                    self.mostrar_mensaje(f"Servidor: {mensaje}")
            except Exception:
                self.mostrar_mensaje("Conexión con el servidor perdida.")
                break

    def mostrar_mensaje(self, mensaje):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, mensaje + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatCliente(root)
    root.mainloop()
