from sqlalchemy.ext.asyncio import AsyncSession

from .seriveces.users import UserService
from .seriveces.reports import ReportService
from .seriveces.admins import AdminService
from .seriveces.forms import FormService

class DBConnector:
    def __init__(self, session: AsyncSession) -> None:
        self.users = UserService(session)
        self.reports = ReportService(session)
        self.admins = AdminService(session)
        self.forms = FormService(session)
