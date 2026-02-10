#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bcrypt

passwords = {
    'admin': 'admin',
    'sucursal1': 'sucursal1',
    'sucursal2': 'sucursal2'
}

print("Hashes bcrypt generados:\n")
for user, password in passwords.items():
    hash_val = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f'{user}:{hash_val}')
