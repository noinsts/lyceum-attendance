from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from ..schemas.user import UserSchema
from ..models.users import UserModel
from ..models.reports import ReportModel


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_user(self, data: UserSchema) -> None:
        try:
            existing_user = await self.session.get(UserModel, data.user_id)
            user_data = data.model_dump()
            if existing_user:
                for k, v in user_data.items():
                    setattr(existing_user, k, v)
            else:
                self.session.add(UserModel(**user_data))
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        
    async def get_user(self, user_id: int) -> Optional[UserModel]:
        return (await self.session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )).scalar_one_or_none()
    
    async def get_users_without_reports(self, reports: List[ReportModel]) -> List[UserModel]:
        forms = [r.form for r in reports]
        return (await self.session.execute(
            select(UserModel).where(UserModel.form.notin_(forms))
        )).scalars().all()
