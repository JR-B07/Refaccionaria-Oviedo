import os
import re
import traceback
from sqlalchemy import create_engine, text


def build_from_env_or_file():
    # Preferir variable de entorno
    env_db = os.getenv('DATABASE_URL')
    if env_db:
        return env_db

    # Leer valores por defecto desde app/core/config.py sin importar el paquete
    cfg_path = os.path.join('app', 'core', 'config.py')
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(cfg_path)

    text_cfg = open(cfg_path, 'r', encoding='utf-8').read()

    def find(key):
        m = re.search(rf"{key}[^\n=]*=\s*[\"']([^\"']+)[\"']", text_cfg)
        return m.group(1).strip() if m else None

    server = (find('MYSQL_SERVER') or 'localhost').strip()
    user = (find('MYSQL_USER') or 'root').strip()
    password = (find('MYSQL_PASSWORD') or '').strip()
    db = (find('MYSQL_DB') or 'refaccionaria_db').strip()
    port = (find('MYSQL_PORT') or '3306').strip()

    # Construir URL sin contraseña si está vacía
    if password:
        return f"mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
    else:
        return f"mysql+pymysql://{user}@{server}:{port}/{db}"


def main():
    try:
        db_url = build_from_env_or_file()
        print('Usando DATABASE_URL =', db_url)
        engine = create_engine(db_url)
        with engine.connect() as conn:
            r = conn.execute(text('SELECT 1'))
            print('Conexión OK, SELECT 1 =>', r.scalar())
    except Exception:
        print('ERROR al conectar a la DB:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
