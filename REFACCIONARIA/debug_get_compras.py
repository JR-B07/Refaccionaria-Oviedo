#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de debug para GET /compras"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

print("Intentando GET /compras...")
try:
    resp = requests.get(f"{BASE_URL}/compras")
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}")
    print(f"Text: {resp.text}")
    print(f"Content: {resp.content}")
except Exception as e:
    print(f"Error: {e}")
