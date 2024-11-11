from abc import ABCMeta, abstractmethod

from .base_manager_context import BaseManagerContextFWDI
from .base_service import BaseServiceFWDI


class BaseUserRepositoryFWDI(BaseServiceFWDI, metaclass=ABCMeta):
    
    @abstractmethod
    def get_all(self, manager_db_context: BaseManagerContextFWDI) -> list[dict]:
        ...

    @abstractmethod
    def get_user_scopes(self, email, manager_db_context: BaseManagerContextFWDI) -> list[str]:
        ...