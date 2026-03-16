from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.forms import FormsModel


class FormService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_form_names(self) -> List[str]:
        return (await self.session.execute(
            select(FormsModel.name)
        )).scalars().all()
