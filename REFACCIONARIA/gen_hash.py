import hashlib

password = "admin"
hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(hashed)
