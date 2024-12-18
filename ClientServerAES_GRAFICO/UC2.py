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


# Funciones de cifrado/descifrado
def encrypt_text_rsa(cifra_publica, text):
    encrypted_text = cifra_publica.encrypt(text.encode())
    return base64.b64encode(encrypted_text).decode("utf-8")


def decrypt_text_rsa(cifra_privada, encrypted_text):
    encrypted_data = base64.b64decode(encrypted_text)
    decrypted_text = cifra_privada.decrypt(encrypted_data)
    return decrypted_text.decode("utf-8")


class ChatServidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor UC2 - Comunicación RSA")
        self.root.geometry("700x800")
        self.root.config(bg="#2B2B2B")

        # Variables de conexión
        self.servidor = None
        self.cliente_conectado = None
        self.direccion_cliente = None
        self.cifra_privada = cargar_clave_privada("clave_privada.pem")
        self.cifra_publica_cliente = cargar_clave_publica("clave_publica.pem")
        self.servidor_activo = False  # Estado del servidor

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ttk.Label(
            self.root, text="Servidor UC2 - Comunicación Cifrada", font=("Arial", 20, "bold"), background="#2B2B2B", foreground="white"
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

        self.start_button = ttk.Button(self.root, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Parar Servidor", command=self.parar_servidor)
        self.stop_button.pack(pady=5)

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

    def iniciar_servidor(self):
        ip_servidor = self.server_ip_entry.get()
        puerto_servidor = int(self.server_port_entry.get())

        try:
            self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.servidor.bind((ip_servidor, puerto_servidor))
            self.servidor.listen(5)
            self.servidor_activo = True
            messagebox.showinfo("Servidor", f"Servidor iniciado en {ip_servidor}:{puerto_servidor}")

            threading.Thread(target=self.aceptar_conexiones, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")

    def parar_servidor(self):
        if self.servidor_activo:
            if self.cliente_conectado:
                self.cliente_conectado.close()
                self.cliente_conectado = None

            self.servidor.close()
            self.servidor = None
            self.servidor_activo = False
            messagebox.showinfo("Servidor", "Servidor detenido.")
        else:
            messagebox.showwarning("Advertencia", "El servidor no está activo.")

    def aceptar_conexiones(self):
        while self.servidor_activo:
            try:
                self.cliente_conectado, self.direccion_cliente = self.servidor.accept()
                self.mostrar_mensaje(f"Cliente conectado desde {self.direccion_cliente}")

                # Inicia un hilo para recibir mensajes del cliente
                threading.Thread(target=self.recibir_mensajes, daemon=True).start()
            except Exception:
                break

    def recibir_mensajes(self):
        while self.servidor_activo and self.cliente_conectado:
            try:
                datos = self.cliente_conectado.recv(1024)
                if datos:
                    mensaje = decrypt_text_rsa(self.cifra_privada, datos.decode())
                    self.mostrar_mensaje(f"Cliente: {mensaje}")
            except Exception:
                self.mostrar_mensaje("Conexión con el cliente perdida.")
                break

    def enviar_mensaje(self):
        if not self.cliente_conectado:
            messagebox.showwarning("Advertencia", "No hay cliente conectado.")
            return

        mensaje = self.message_entry.get()
        if not mensaje:
            messagebox.showwarning("Advertencia", "Por favor, escribe un mensaje.")
            return

        try:
            mensaje_cifrado = encrypt_text_rsa(self.cifra_publica_cliente, mensaje)
            self.cliente_conectado.send(mensaje_cifrado.encode())
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
