import bcrypt

# Generar hash para "admin"
password = "admin"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(f"Hash generado para '{password}':")
print(hashed.decode('utf-8'))

# Verificar el hash actual en la BD
hash_en_bd = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIvAprzO3i"
if bcrypt.checkpw(password.encode('utf-8'), hash_en_bd.encode('utf-8')):
    print(f"\n✅ El hash en BD corresponde a la contraseña '{password}'")
else:
    print(f"\n❌ El hash en BD NO corresponde a la contraseña '{password}'")
