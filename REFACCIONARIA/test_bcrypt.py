import hashlib

# Generar hash para "admin"
password = "admin"
hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(f"Hash generado para '{password}':")
print(hashed)

# Verificar el hash actual en la BD
hash_en_bd = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # SHA256 de "admin"
if hashed == hash_en_bd:
    print(f"\n✅ El hash en BD corresponde a la contraseña '{password}'")
else:
    print(f"\n❌ El hash en BD NO corresponde a la contraseña '{password}'")
