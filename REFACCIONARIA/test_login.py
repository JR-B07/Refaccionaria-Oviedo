import asyncio
from app.api.v1.endpoints import auth
from app.core.database import SessionLocal

async def main():
    db = SessionLocal()
    try:
        req = auth.LoginRequest(username="admin", password="admin")
        result = await auth.login(req, db)
        print(result)
    except Exception as e:
        print("ERROR:", type(e).__name__, e)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
