from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.leetcode_api import LeetCodeAPI
from .models import LeetcodeTask, Difficulty
from sqlalchemy import select


class TaskQuery:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, user_id: int):
        query = select(LeetcodeTask).filter_by(user_id=user_id)
        res = await self.session.execute(query)
        return res

    async def get_single(self, task_id: int):
        return await self.session.get_one(LeetcodeTask, task_id)

    async def create(self, api: LeetCodeAPI, link, user_id: int):
        data = await api.get_problem_detail(link)
        leetcode_task = LeetcodeTask(title=data["title"], difficulty=Difficulty(
            data["difficulty"]), link=data["link"], user_id=user_id)
        self.session.add(leetcode_task)
        await self.session.commit()
        await self.session.refresh(leetcode_task)
        return leetcode_task.task_id

    async def delete(self, task_id: int):
        task = await self.get_single(task_id)
        await self.session.delete(task)
