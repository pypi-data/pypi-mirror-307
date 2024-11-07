import hashlib
from typing import TypeVar
from uuid import uuid4
from Application.Abstractions.base_main_menu import BaseManagerContextMenu
from Domain.Enums.enum_type_menu import TypeMenu

_Child = TypeVar('_Child', bound='ManagerContextMenu')

class ManagerContextMenu(BaseManagerContextMenu):
    
    count: int = 0

    def __init__(self, name: str, context: str, url: str, type_menu: TypeMenu, context_for_vector: str):
        super().__init__()
        self.name = name
        self.context = context
        self.context_for_vector = context_for_vector
        self.url = url
        self.lst_child: list[ManagerContextMenu] = []
        self.type_menu: TypeMenu = type_menu
        self.total_name = ""

    def add_child(self, child:_Child):
        self.lst_child.append(child)

    def load_menu_v2(self, list_menu: list, total_name: str):

        if self.context != '':
            ManagerContextMenu.count += 1
            list_menu.append({"id": ManagerContextMenu.count,
                              'name': self.name,
                              'context_for_vector': total_name + self.context_for_vector,
                              'context': self.context,
                              'url': self.url,
                              'total_name': total_name,
                              'hash': self.get_hash(self.context)})
        else:
            if self.name != "Содержание":
                total_name += self.name + "."

        for child in self.lst_child:
            child.load_menu_v2(list_menu, total_name)

    def get_hash(self, context: str):
        context = context
        check_sum_context = hashlib.md5(context.encode('utf-8')).hexdigest()

        return check_sum_context