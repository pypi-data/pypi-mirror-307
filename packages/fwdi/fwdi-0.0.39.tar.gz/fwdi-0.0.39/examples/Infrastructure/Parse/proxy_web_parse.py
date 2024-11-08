from Application.Abstractions.base_proxy_web_parse import BaseProxyWebParse
from Application.Abstractions.base_web_parse import BaseWebParse
from Infrastructure.Parse.web_parse_bsp import WebParseBSP
from Infrastructure.Parse.web_parse_standart import WebParseStand



class ProxyWebParse(BaseProxyWebParse):

    def get_parse_stand(self)->BaseWebParse:
        return WebParseStand()
    
    def get_parse_bsp(self)->BaseWebParse:
        return WebParseBSP()