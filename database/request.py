from sqlalchemy import select, insert, delete, update

from database.engine import async_session
from models import User, Task
from models.models import StatusTask


async def insert_user(user_id, username):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.user_id == user_id))
    if not user:
        await session.execute(
            insert(User).values(user_id=user_id, username=username)
        )
        await session.commit()


async def insert_task(title, description, user_id):
    async with async_session() as session:
        await session.execute(
            insert(Task).values(title=title, description=description,
                                user_id=user_id)
        )
        await session.commit()


async def get_tasks_list(user_id):
    async with async_session() as session:
        results = await session.scalars(
            select(Task).where(Task.user_id == user_id)
        )
        return results


async def get_current_task_for_user(task_id):
    async with async_session() as session:
        results = await session.scalar(
            select(Task).where(Task.id == task_id)
        )
        return results


async def delete_current_task(task_id):
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.id == task_id))
        await session.commit()


async def update_current_task(title: str, description: str, task_id: int):
    async with async_session() as session:
        await session.execute(
            update(Task)
            .filter_by(id=task_id)
            .values(title=title, description=description,
                    status=StatusTask.not_done)
        )
        await session.commit()


async def update_status_task(status, task_id):
    async with async_session() as session:
        await session.execute(
            update(Task)
            .filter_by(id=task_id, status=StatusTask.not_done)
            .values(status=status)
        )
        await session.commit()
