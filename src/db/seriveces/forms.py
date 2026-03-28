from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.forms import FormsModel
from ..schemas.form import FormSchema


class FormService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_form_names(self) -> List[str]:
        return (await self.session.execute(
            select(FormsModel.name)
        )).scalars().all()
    
    async def add_form(self, data: FormSchema) -> None:
        self.session.add(FormsModel(**data.model_dump()))
        await self.session.commit()

    async def get_form_by_name(self, name: str) -> FormSchema | None:
        return (await self.session.execute(
            select(FormsModel).where(FormsModel.name == name)
        )).scalar_one_or_none()
