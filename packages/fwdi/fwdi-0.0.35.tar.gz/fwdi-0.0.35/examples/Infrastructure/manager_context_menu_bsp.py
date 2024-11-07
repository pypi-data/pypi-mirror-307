

from Application.Abstractions.base_main_menu import BaseManagerContextMenu


class ManagerContextMenuBSP(BaseManagerContextMenu):

    def __init__(self, name: str, context: str, url: str):
        super().__init__()
        self.name: str = name
        self.context: str = context
        self.url: str = url
        self.lst_child: list[ManagerContextMenuBSP] = []
        self.count: int = 0

    def add_child(self, child):
        self.lst_child.append(child)

    def load_menu_v2(self, list_menu: list, total_name=''):

        if self.context != '':
            self.count += 1
            list_menu.append({
                'id': self.count,
                'name': self.name,
                'context': self.context,
                'context_for_llm': self.context,
                'url': self.url,
                'total_name': total_name
            })
        else:
            if self.name != 'Содержание':
                total_name += self.name + '.'

        for child in self.lst_child:
            child.load_menu_v2(list_menu, total_name)
    
    def get_hash(self, context: str):
        pass