"""Create (or promote) an admin user: python -m scripts.create_admin EMAIL PASSWORD

Run `alembic upgrade head` first.
"""

import asyncio
import sys

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import User


async def main(email: str, password: str) -> None:
    async with SessionLocal() as session:
        user = await session.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, hashed_password=hash_password(password))
            session.add(user)
        user.is_admin = True
        await session.commit()
    print(f"Admin ready: {email}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
