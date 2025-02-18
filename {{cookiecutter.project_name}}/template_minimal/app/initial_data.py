"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio
from typing import Optional

from sqlalchemy import select

from app.core import config, security
from app.models import User
from app.session import async_session


async def main() -> None:
    print("Start initial data")
    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.email == config.settings.FIRST_SUPERUSER_EMAIL)
        )
        user: Optional[User] = result.scalars().first()

        if user is None:
            new_superuser = User(
                email=config.settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=security.get_password_hash(
                    config.settings.FIRST_SUPERUSER_PASSWORD
                ),
                full_name=config.settings.FIRST_SUPERUSER_EMAIL,
            )
            session.add(new_superuser)
            await session.commit()
            print("Superuser was created")
        else:
            print("Superuser already exists in database")

        print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
