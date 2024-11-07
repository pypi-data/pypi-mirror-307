from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
import requests


class BaseWebParseTools(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def url_request(url: str) -> requests.Request:
        pass

    @abstractmethod
    def parse_req(parse_req:requests.Response) -> BeautifulSoup:
        pass

    @abstractmethod
    def clear_text_for_vector(text: str) -> str:
        pass