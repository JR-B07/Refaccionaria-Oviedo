import bcrypt

# Prueba de hash y verificación
password = "prueba123"
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print("Hash generado:", hash.decode())

# Verificar contraseña
if bcrypt.checkpw(password.encode(), hash):
    print("✅ Contraseña verificada correctamente")
else:
    print("❌ Contraseña incorrecta")
