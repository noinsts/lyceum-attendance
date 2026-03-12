from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..schemas.report import ReportSchema
from ..models.reports import ReportModel


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_report(self, data: ReportSchema) -> None:
        try:
            self.session.add(ReportModel(**data.model_dump()))
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def get_reports_by_day(self, date: datetime) -> List[ReportModel]:
        return (await self.session.execute(
            select(ReportModel).where(ReportModel.date == date)
        )).scalars().all()
