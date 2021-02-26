from requests import get
from bs4 import BeautifulSoup


class HttpBaseException(Exception):
    pass


def getObject(url: str):

    req = get(url=url)
    if not req.ok:
        raise HttpBaseException('the request has encounded and issue')

    html = req.text
    if isinstance(html, str) == False:
        raise HttpBaseException('the request response dose not have a body')

    req.close()
    bs = BeautifulSoup(html, 'html.parser')
    return bs
