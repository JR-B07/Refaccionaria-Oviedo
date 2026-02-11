import hashlib

# Prueba de hash y verificación
password = "prueba123"
hash = hashlib.sha256(password.encode()).hexdigest()

print("Hash generado:", hash)

# Verificar contraseña
verify_hash = hashlib.sha256(password.encode()).hexdigest()
if verify_hash == hash:
    print("✅ Contraseña verificada correctamente")
else:
    print("❌ Contraseña incorrecta")
