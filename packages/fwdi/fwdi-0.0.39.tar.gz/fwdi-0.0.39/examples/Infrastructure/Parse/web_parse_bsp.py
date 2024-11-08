import bs4
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Application.Abstractions.base_main_menu import BaseManagerContextMenu
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.Abstractions.base_web_parse import BaseWebParse
from Application.Abstractions.base_web_parse_tools import BaseWebParseTools
from Infrastructure.Config.web_parse_bsp_config import WebParseBSPConfig
from Infrastructure.manager_context_menu_bsp import ManagerContextMenuBSP


base_url = 'https://its.1c.ru'
start_url = 'https://its.1c.ru/db/v8std#browse:13:-1'

class WebParseBSP(BaseWebParse):

    def parse(self, web_parse_tools: BaseWebParseTools, config: WebParseBSPConfig, text_tools: BaseTextTools) -> list[dict]:
        try:
            driver = self.__create_driver()
            driver.get("https://its.1c.ru/user/auth?backurl=%2F")
            driver.find_element(By.ID, 'login_portal').click()

            username_input = driver.find_element(By.ID, 'username')
            username_input.clear()
            username_input.send_keys(config.login)

            password_input = driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(config.password)
            driver.find_element(By.ID, 'loginButton').click()
            res = requests.get('https://its.1c.ru/db/bsp3110doc')
            menu = ManagerContextMenuBSP(url='https://its.1c.ru/db/bsp3110doc', name='Содержание', context='')
            driver_cookies = driver.get_cookies()
            cookies = {}
            for cookie in driver_cookies:
                cookies[cookie['name']] = cookie['value']
            soup = web_parse_tools.parse_req(res)
            items = soup.find('li', class_='expanded active').find('ul').find_all('li', recursive=False)
            self.__iteration_items_menu(items_menu=items[:1], parent=menu, cookies=cookies)

            lst_doc = []
            menu.load_menu_v2(lst_doc)

            lst_final_doc_sent_summ = []
            for index, doc in enumerate(lst_doc):
                dct_doc = {'doc_id': index, 'name': doc['name'], 'context_for_llm': doc['context'], 'context': text_tools.clean_and_repack_text(doc['context']), 'url': doc['url'], 'article': doc['total_name']}
                lst_final_doc_sent_summ.append(dct_doc)

            #data_frame = pd.DataFrame(lst_doc, columns=['id', 'name', 'context', 'url', 'total_name'])
            #path_db = 'ParseData.pkl'
            #data_frame.to_pickle(path_db)

            return lst_final_doc_sent_summ

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def __iter_for_tags(self, lst_tags_document: list, name_document: str, flag = False) -> str:
        context = ''
        for tag in lst_tags_document:
            if tag != '\n' and tag.name != 'script' and tag.name != 'hr':
                if tag.name == 'div':
                    tags_stage_2 = tag.children
                    lst_tag_stage_2 = list(tags_stage_2)
                    context = self.__iter_for_tags(lst_tag_stage_2, name_document)
                    if context != '':
                        return context

                if tag.name == 'section':
                    if name_document.replace('-',' ').replace('.', '').replace(',', '').lower() in tag['id'].replace('-', ' ').replace('.', '').replace('_', '').lower():
                        context = tag.text
                        break


                elif flag and tag.name != 'a' and tag.name != 'h1':
                    if tag.text is not None:
                        context += tag.text

                elif tag.name == 'a' or tag.name == 'h1':
                    if tag.name == 'a' and tag.text.lower() == name_document.lower():
                        flag = True
                    elif flag and tag.name == 'a':
                        flag = False
                        break
                    elif tag.name == 'h1' and tag.text.lower() == name_document.lower():
                        flag = True

        if context != "":
            context = ' '.join(context.split())
            context = f'{name_document}\n' + context

        return context


    def __create_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        return driver

    def __create_child(self, item_menu:bs4.element.Tag, parent: BaseManagerContextMenu, context='') -> BaseManagerContextMenu:
        name_item_menu = item_menu.a.text
        url_item_menu = f'https://its.1c.ru{item_menu.a["href"]}'
        item_menu = ManagerContextMenuBSP(url=url_item_menu, name=name_item_menu, context=context)
        parent.add_child(item_menu)

        return item_menu

    def __iteration_items_menu(self, items_menu: bs4.element.ResultSet, parent: BaseManagerContextMenu, cookies:dict, web_parse_tools: BaseWebParseTools):
        for item in items_menu:
            item_menu = self.__create_child(item, parent)
            if item.get('class') == ['collapsed']:
                items_layer = item.find('ul', recursive=False).find_all('li', recursive=False)
                self.__iteration_items_menu(items_layer, item_menu, cookies)
            else:
                url_item_menu = f'https://its.1c.ru{item.a["href"]}'
                res = requests.get(url_item_menu, cookies=cookies)
                soup_text = web_parse_tools.parse_req(res)

                tags = soup_text.find('div', class_='filter_place')
                if tags is None:
                    tags = soup_text.find('body', class_='bsp3110doc paywall')
                    if tags is None:
                        tags = soup_text.find('body', class_='bsp320doc paywall')
                if tags is not None:
                    lst_tags = list(tags.children)
                    name_doc = item.text
                    context = self.__iter_for_tags(lst_tags, name_doc)
                    if context != '':
                        self.__create_child(item, parent, context=context)
                else:
                    src = soup_text.find('iframe', class_='l mimic_scroll')['src']
                    res = requests.get(f'https://its.1c.ru{src}', cookies=cookies)
                    soup_text_doc = web_parse_tools.parse_req(res)

                    tags = soup_text_doc.find('div', class_='filter_place')
                    if tags is None:
                        tags = soup_text_doc.find('body', class_='bsp3110doc paywall')
                        if tags is None:
                            tags = soup_text_doc.find('body', class_='bsp320doc paywall')
                    if tags is not None:
                        lst_tags = list(tags.children)
                        name_doc = item.text
                        context = self.__iter_for_tags(lst_tags, name_doc)
                        if context != '':
                            self.__create_child(item, parent, context=context)