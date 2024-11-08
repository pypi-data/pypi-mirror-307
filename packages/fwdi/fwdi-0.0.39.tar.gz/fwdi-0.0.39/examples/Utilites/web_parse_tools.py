import re
from bs4 import BeautifulSoup
import requests

from Application.Abstractions.base_web_parse_tools import BaseWebParseTools


st_accept = "text/html"
st_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko)" \
        " Version/15.4 Safari/605.1.15 "

headers = {
    "Accept": st_accept,
    "User-Agent": st_user_agent
}



class WebParseTools(BaseWebParseTools):

    def url_request(url: str) -> requests.Response:

        req = requests.get(url, headers)
        if req.status_code == 200:
            return req
        return None
    
    def parse_req(parse_req) -> BeautifulSoup:

        src = parse_req.text
        soup = BeautifulSoup(src, 'html.parser')
        return soup
    
    def clear_text_for_vector(text: str) -> str:
        matches = re.finditer(r"(См|см[\.][также]?[:]?)(\W*)", text, flags=re.ASCII)

        for matchNum, match in enumerate(matches, start=1):
            text = text.replace(str(match.group()), '')

        text = re.sub(r'\#std(\d*)?', " ",  text, 0,  re.MULTILINE)
    
        return text
