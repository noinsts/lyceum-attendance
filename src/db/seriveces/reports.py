from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

from ..schemas.report import ReportSchema
from ..models.reports import ReportModel


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_report(self, data: ReportSchema) -> None:
        try:
            query = insert(ReportModel).values(
                **data.model_dump()
            )
            query = query.on_conflict_do_update(
                index_elements=["form", "date"],
                set_={
                    "absentees": data.absentees,
                    "patients": data.patients,
                    "total": data.total
                }
            )
            await self.session.execute(query)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def get_reports_by_day(self, date: datetime) -> List[ReportModel]:
        return (await self.session.execute(
            select(ReportModel).where(ReportModel.date == date)
        )).scalars().all()
