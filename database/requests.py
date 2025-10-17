from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .db_engine import async_session, engine
from .tables import Base, Users


def connection(function):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await function(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


@connection
async def get_user(user_tg_id: int, session: AsyncSession):
    user = await session.scalar(select(Users).where(Users.id == user_tg_id))
    return user


@connection
async def new_user(user_tg_id: int, name: str, tg_username: str, register_date: date, referral_id: int | None,
                   session: AsyncSession) -> Users:
    user = Users(
        id=user_tg_id,
        name=name,
        tg_username=tg_username,
        referral_id=referral_id,
        register_date=register_date,
        balance=0,
    )
    session.add(user)
    await session.commit()
    user = await get_user(user_tg_id)
    return user


@connection
async def update_name(user_tg_id: int, name: str, session: AsyncSession):
    stmt = update(Users).where(Users.id == user_tg_id).values(name=name)
    await session.execute(stmt)
    await session.commit()


@connection
async def new_referral(user_tg_id: int, session: AsyncSession):
    stmt = update(Users).where(Users.id == user_tg_id).values(is_referral=True)
    await session.execute(stmt)
    await session.commit()


@connection
async def get_referrals(user_tg_id: int, session: AsyncSession):
    response = await session.scalars(select(Users).where(Users.referral_id == user_tg_id))
    return response.all()
