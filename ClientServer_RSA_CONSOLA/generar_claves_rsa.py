from Crypto.PublicKey import RSA                              # IMPORTA EL MODULO RSA DE LA BIBLIOTECA PYCRYPTODOME

def generar_claves_rsa():
    clave = RSA.generate(2048)                                # GENERA DOS CLAVES RSA DE 2048 BITS
    clave_publica = clave.publickey().export_key()            # SE OBTIENE LA CLAVE PUBLICA Y SE EXPORTA EN FORMATO PEM
    clave_privada = clave.export_key()                        # SE EXPORTA LA CLAVE PRIVADA EN FORMATO PEM

    with open("clave_publica.pem", "wb") as f:                # ABRE LA CLAVE PUBLICA EN MODO ESCRITURA BINARIA
        f.write(clave_publica)                                # ESCRIBE LA CLAVE PUBLICA EXPORTADA EN ESTE ARCHIVO 

    with open("clave_privada.pem", "wb") as f:                # ABRE LA CLAVE PRIVADA EN MODO ESCRITURA BINARIA
        f.write(clave_privada)                                # ESCRIBE LA CLAVE PRIVADA EXPORTADA EN ESTE ARCHIVO

if __name__ == "__main__":
    generar_claves_rsa()
    print("Claves RSA generadas y guardadas.")