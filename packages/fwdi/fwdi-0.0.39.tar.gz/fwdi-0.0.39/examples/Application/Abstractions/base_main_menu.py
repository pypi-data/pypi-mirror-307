from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


class BaseManagerContextMenu(BaseServiceFWDI, metaclass=ABCMeta):
    
    @abstractmethod
    def add_child(self, child) -> None: 
        pass

    @abstractmethod
    def load_menu_v2(self, list_menu: list, total_name="") -> list:
        pass

    @abstractmethod
    def get_hash(self, context: str) -> str:
        pass