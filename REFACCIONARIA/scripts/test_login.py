import json
import urllib.request

url = "http://127.0.0.1:8000/api/v1/auth/login"
data = json.dumps({"username": "admin", "password": "admin123"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(resp.status)
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as he:
    print('HTTP ERROR:', he.code)
    try:
        print(he.read().decode('utf-8'))
    except Exception:
        pass
except Exception as e:
    print('ERROR:', e)
