from fwdi.Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.Abstractions.base_web_parse_tools import BaseWebParseTools
from Utilites.tools import TextTools, PostProccessingText
from Utilites.web_parse_tools import WebParseTools

class DependencyInjection():
    def AddUtils(services:BaseServiceCollectionFWDI):
        services.AddTransient(BaseTextTools, TextTools)
        services.AddTransient(PostProccessingText)
        services.AddTransient(BaseWebParseTools, WebParseTools)
