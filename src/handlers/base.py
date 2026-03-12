from abc import ABC, abstractmethod

from aiogram import Router

class BaseHandler(ABC):
    def __init__(self):
        self.router = Router()
        self.register_handlers()
        
    @abstractmethod
    def register_handlers(self) -> None:
        pass

    def get_router(self) -> Router:
        return self.router
