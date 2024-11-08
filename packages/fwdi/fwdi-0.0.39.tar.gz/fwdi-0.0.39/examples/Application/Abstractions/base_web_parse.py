from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.Abstractions.base_web_parse_tools import BaseWebParseTools
from Infrastructure.Config.web_parse_bsp_config import WebParseBSPConfig


class BaseWebParse(BaseServiceFWDI, metaclass=ABCMeta):
    @abstractmethod
    def parse(self, web_parse_tools: BaseWebParseTools, config: WebParseBSPConfig, text_tools: BaseTextTools) -> list[dict]:
        pass