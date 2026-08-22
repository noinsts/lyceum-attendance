from typing import List
from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.food import FoodSchema
from ..models.food import FoodModel


class FoodService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_report(self, data: FoodSchema) -> None:
        try:
            query = insert(FoodModel).values(**data.model_dump())
            query = query.on_conflict_do_update(
                index_elements=["form", "date"],
                set_={
                    "count": data.count,
                    "total": data.total,
                }
            )
            await self.session.execute(query)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def get_reports_by_day(self, date_: date) -> List[FoodModel]:
        return (await self.session.execute(
            select(FoodModel).where(FoodModel.date == date_)
        )).scalars().all()
