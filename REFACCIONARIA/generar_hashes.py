#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

passwords = {
    'admin': 'admin',
    'sucursal1': 'sucursal1',
    'sucursal2': 'sucursal2'
}

print("Hashes SHA256 generados:\n")
for user, password in passwords.items():
    hash_val = hashlib.sha256(password.encode()).hexdigest()
    print(f'{user}:{hash_val}')
