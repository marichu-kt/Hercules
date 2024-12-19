from Crypto.PublicKey import RSA

def generar_clave_cliente():
    clave_cliente = RSA.generate(2048)
    clave_publica = clave_cliente.publickey().export_key()

    with open("clave_publica.pem", "wb") as pub_file:
        pub_file.write(clave_publica)

    with open("clave_privada.pem", "wb") as priv_file:
        priv_file.write(clave_cliente.export_key())

if __name__ == "__main__":
    generar_clave_cliente()
    print("Claves públicas y privadas generadas y guardadas con éxito.")
