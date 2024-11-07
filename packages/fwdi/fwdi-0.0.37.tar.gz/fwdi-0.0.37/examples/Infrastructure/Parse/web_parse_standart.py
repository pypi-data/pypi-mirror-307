from tqdm import tqdm
from Application.Abstractions.base_web_parse import BaseWebParse
from Application.Abstractions.base_web_parse_tools import BaseWebParseTools
from Domain.Enums.enum_type_menu import TypeMenu
from Infrastructure.manager_context_menu import ManagerContextMenu
from Application.Abstractions.base_text_tools import BaseTextTools
from Infrastructure.Config.web_parse_bsp_config import WebParseBSPConfig


base_url = 'https://its.1c.ru'
start_url = 'https://its.1c.ru/db/v8std#browse:13:-1'

class WebParseStand(BaseWebParse):

    def parse(self, web_parse_tools: BaseWebParseTools, config: WebParseBSPConfig, text_tools: BaseTextTools) -> list[dict]:
        menu = ManagerContextMenu(url=start_url, name='Содержание', context='', context_for_vector='', type_menu=TypeMenu.FOLDER)
        req = web_parse_tools.url_request(start_url)
        soup = web_parse_tools.parse_req(req)
        lst_href_1layer = soup.find_all(class_=['folder collapsed', 'folder leaf'])

        with tqdm(total=len(lst_href_1layer), desc="Parse Web Resource") as p_bar:

            for href_1layer in lst_href_1layer[:1]:

                topic_menu = ManagerContextMenu(url=f'{base_url}{href_1layer.a["href"]}',
                                    name=href_1layer.a.text,
                                    context='',
                                    context_for_vector='',
                                    type_menu=TypeMenu.FOLDER)
                menu.add_child(topic_menu)

                req_1layer = web_parse_tools.url_request(f'{base_url}{href_1layer.a["href"]}')
                soup_1layer = web_parse_tools.parse_req(req_1layer)
                lst_href_2layer = soup_1layer.find(class_="nav list").find_all('li')
                for href_2layer in lst_href_2layer:
                    if href_2layer['class'][0] == 'folder':

                        catalog_menu = ManagerContextMenu(url=f'{base_url}{href_2layer.a["href"]}',
                                                name=href_2layer.a.text,
                                                context='',
                                                context_for_vector='',
                                                type_menu=TypeMenu.FOLDER)
                        topic_menu.add_child(catalog_menu)

                        req_3layer = web_parse_tools.url_request(f'{base_url}{href_2layer.a["href"]}')
                        soup_3layer = web_parse_tools.parse_req(req_3layer)
                        lst_href_3layer = soup_3layer.find(class_="nav list").find_all('li')
                        for href_3layer in lst_href_3layer:
                            req_4layer = web_parse_tools.url_request(f'{base_url}{href_3layer.a["href"]}')
                            soup_4layer = web_parse_tools.parse_req(req_4layer)
                            text_title = soup_4layer.body.h1['title']
                            lst_href_4layer = soup_4layer.find(class_='l')

                            if ' ' in lst_href_4layer["href"]:
                                lst_href_4layer["href"] = lst_href_4layer["href"].replace(' ', '%C2%A0')

                            req_text = web_parse_tools.url_request(f'{base_url}{lst_href_4layer["href"]}')
                            soup_text = web_parse_tools.parse_req(req_text)
                            text = (' '.join(soup_text.text.split()))

                            text = text.replace(':: Система стандартов и методик разработки конфигураций для платформы 1С:Предприятие 8', '')
                            text = text.replace(f"{text_title} ", '', 1)

                            text_for_vector = (' '.join(web_parse_tools.clear_text_for_vector(soup_text.text).split()))

                            text_for_vector = text_for_vector.replace(':: Система стандартов и методик разработки конфигураций для платформы 1С:Предприятие 8', '')
                            text_for_vector = text_for_vector.replace(f"{text_title} ", '', 1)

                            doc_menu = ManagerContextMenu(url=f'{base_url}{lst_href_4layer["href"]}',
                                                name=text_title,
                                                context=text,
                                                context_for_vector=text_for_vector,
                                                type_menu=TypeMenu.DOC_ICON)
                            catalog_menu.add_child(doc_menu)

                    else:

                        req_doc = web_parse_tools.url_request(f'{base_url}{href_2layer.a["href"]}')
                        soup_doc = web_parse_tools.parse_req(req_doc)
                        text_title = soup_doc.body.h1['title']
                        href_doc = soup_doc.find(class_='l')
                        req_text = web_parse_tools.url_request(f'{base_url}{href_doc["href"]}')
                        soup_text = web_parse_tools.parse_req(req_text)

                        text = (' '.join(soup_text.text.split()))
                        text = text.replace(':: Система стандартов и методик разработки конфигураций для платформы 1С:Предприятие 8', '')
                        text = text.replace(f"{text_title} ", '', 1)

                        text_for_vector = (' '.join(web_parse_tools.clear_text_for_vector(soup_text.text).split()))

                        text_for_vector = text_for_vector.replace(':: Система стандартов и методик разработки конфигураций для платформы 1С:Предприятие 8', '')
                        text_for_vector = text_for_vector.replace(f"{text_title} ", '', 1)

                        if ' ' in href_doc["href"]:
                            href_doc["href"] = href_doc["href"].replace(' ', '%C2%A0')

                        catalog_menu = ManagerContextMenu(url=f'{base_url}{href_doc["href"]}',
                                                name=text_title,
                                                context=text,
                                                context_for_vector=text_for_vector,
                                                type_menu=TypeMenu.DOC_ICON)
                        topic_menu.add_child(catalog_menu)

                p_bar.update(1)

        lst_menu = []
        menu.load_menu_v2(lst_menu, "")
        # data_frame = pd.DataFrame(lst_menu, columns=['id', 'name', 'context', 'context_for_vector', 'url', "total_name"])
        # data_frame.to_excel("test.xlsx")
        return lst_menu