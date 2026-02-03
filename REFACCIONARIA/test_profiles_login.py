import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
TEST_TOKEN_URL = f"{BASE_URL}/api/v1/auth/test-token"

USERS = [
    ("admin", "admin"),
    ("sucursal1", "sucursal1"),
    ("sucursal2", "sucursal2"),
]


def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def get_json(url, headers=None):
    req = urllib.request.Request(url, method="GET")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def main():
    results = []
    for username, password in USERS:
        print(f"\n🔐 Probando login: {username}")
        try:
            status, body = post_json(LOGIN_URL, {"username": username, "password": password})
            ok = status == 200 and body.get("success") is True and body.get("access_token")
            token = body.get("access_token") if ok else None
            print(f"   Status: {status}")
            print(f"   Success: {body.get('success')}")
            print(f"   Role: {body.get('user', {}).get('role')}")
            if token:
                t_status, t_body = get_json(TEST_TOKEN_URL, {"Authorization": f"Bearer {token}"})
                print(f"   Test token: {t_body}")
                ok = ok and t_status == 200 and t_body.get("valid") is True
            results.append((username, ok))
        except urllib.error.HTTPError as e:
            print(f"   ❌ HTTPError: {e.code} - {e.read().decode('utf-8')}")
            results.append((username, False))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append((username, False))

    print("\n==============================")
    print("📊 RESUMEN DE PERFILES")
    print("==============================")
    for username, ok in results:
        print(f"{username}: {'✅ OK' if ok else '❌ FAIL'}")

    failed = [u for u, ok in results if not ok]
    if failed:
        print(f"\n⚠️  Perfiles con fallo: {', '.join(failed)}")
    else:
        print("\n🎉 Todos los perfiles funcionan correctamente")


if __name__ == "__main__":
    main()
