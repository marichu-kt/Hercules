import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# Funciones para cargar claves RSA
def cargar_clave_privada(archivo):
    with open(archivo, "rb") as f:
        clave = RSA.import_key(f.read())
    return PKCS1_OAEP.new(clave)


def cargar_clave_publica(archivo):
    with open(archivo, "rb") as f:
        clave = RSA.import_key(f.read())
    return PKCS1_OAEP.new(clave)


# Funciones de descifrado y cifrado
def encrypt_text_rsa(cifra_publica, text):
    encrypted_text = cifra_publica.encrypt(text.encode())
    return base64.b64encode(encrypted_text).decode("utf-8")


def decrypt_text_rsa(cifra_privada, encrypted_text):
    encrypted_data = base64.b64decode(encrypted_text)
    decrypted_text = cifra_privada.decrypt(encrypted_data)
    return decrypted_text.decode("utf-8")


class ChatCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente UC1 - Comunicación RSA")
        self.root.geometry("700x800")
        self.root.config(bg="#2B2B2B")

        # Variables de conexión
        self.cliente = None
        self.conectado = False  # Estado de conexión

        # Claves RSA
        self.cifra_privada = cargar_clave_privada("clave_privada.pem")
        self.cifra_publica_servidor = cargar_clave_publica("clave_publica.pem")

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ttk.Label(
            self.root, text="Cliente UC1 - Comunicación Cifrada", font=("Arial", 20, "bold"), background="#2B2B2B", foreground="white"
        )
        self.title_label.pack(pady=10)

        # Configuración de conexión
        self.config_frame = tk.Frame(self.root, bg="#2B2B2B")
        self.config_frame.pack(pady=10)

        self.server_ip_label = ttk.Label(self.config_frame, text="IP Servidor:", background="#2B2B2B", foreground="white")
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.server_ip_entry = ttk.Entry(self.config_frame, width=20)
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.server_port_label = ttk.Label(self.config_frame, text="Puerto Servidor:", background="#2B2B2B", foreground="white")
        self.server_port_label.grid(row=0, column=2, padx=5, pady=5)
        self.server_port_entry = ttk.Entry(self.config_frame, width=10)
        self.server_port_entry.grid(row=0, column=3, padx=5, pady=5)

        self.connect_button = ttk.Button(self.root, text="Conectar al Servidor", command=self.conectar_servidor)
        self.connect_button.pack(pady=5)

        self.disconnect_button = ttk.Button(self.root, text="Desconectar", command=self.desconectar_servidor)
        self.disconnect_button.pack(pady=5)

        # Área de mensajes
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, font=("Arial", 12), bg="#F5F5F5")
        self.chat_display.pack(pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Entrada de mensajes
        self.message_entry = ttk.Entry(self.root, font=("Arial", 12), width=60)
        self.message_entry.pack(pady=5)

        # Botón para enviar mensajes
        self.send_button = ttk.Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje)
        self.send_button.pack(pady=10)

    def conectar_servidor(self):
        ip_servidor = self.server_ip_entry.get()
        puerto_servidor = int(self.server_port_entry.get())

        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((ip_servidor, puerto_servidor))
            self.conectado = True
            messagebox.showinfo("Cliente", f"Conectado al servidor en {ip_servidor}:{puerto_servidor}")

            # Inicia un hilo para recibir mensajes del servidor
            threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def desconectar_servidor(self):
        if self.conectado:
            self.cliente.close()
            self.conectado = False
            messagebox.showinfo("Cliente", "Desconectado del servidor.")
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
            mensaje_cifrado = encrypt_text_rsa(self.cifra_publica_servidor, mensaje)
            self.cliente.send(mensaje_cifrado.encode())
            self.mostrar_mensaje(f"Tú: {mensaje}")
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

    def recibir_mensajes(self):
        while self.conectado:
            try:
                datos = self.cliente.recv(1024)
                if datos:
                    mensaje = decrypt_text_rsa(self.cifra_privada, datos.decode())
                    self.mostrar_mensaje(f"Servidor: {mensaje}")
            except Exception:
                self.mostrar_mensaje("Conexión perdida con el servidor.")
                self.conectado = False
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
