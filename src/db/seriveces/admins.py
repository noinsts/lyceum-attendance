from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.admins import AdminModel


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_ids(self) -> List[int]:
        return (await self.session.execute(
            select(AdminModel.user_id)
        )).scalars().all()
    
    async def get_name(self, user_id: int) -> Optional[str]:
        return (await self.session.execute(
            select(AdminModel.name).where(AdminModel.user_id == user_id)
        )).scalar_one_or_none()
    
    async def is_admin(self, user_id: int) -> bool:
        return (await self.session.execute(
            select(AdminModel).where(AdminModel.user_id == user_id)
        )).scalar_one_or_none() is not None
