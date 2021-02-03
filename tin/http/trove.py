from os import mkdir
from os.path import isdir, isfile
from time import sleep
from shutil import copyfileobj
from random import randint
from threading import Thread


from requests.api import get
from .base import getObject
from tin.data.commons import mkHex

def getTokens():
    url = "https://thetrove.is/Assets/By%20Artist%20or%20Source/5eTools/currated/Token/"
    obj = getObject(url=url)

    css = '#index-holder__container table#list tbody tr td:first-child a'
    tokens_onSite = []
    for el in obj.select(css):
        
        if el.text.split('.')[-1] in ['png', 'gif', 'jpg']:
            tokens_onSite.append(
                f'{url}{ el["href"] }'
            )
    return tokens_onSite

def downloader(img_addr:str):

    fname = img_addr.split("/")[-1]
    req = get(img_addr, stream=True)
    req.raw.decode_content = True

    if isdir('static/a') == False:
        mkdir('static/a')
    
    if isdir('static/a/tokens') == False:
        mkdir('static/a/tokens')

    if isfile(f'static/a/tokens/{fname}'):
        return f'static/a/tokens/{fname}'
    
    with open(f'static/a/tokens/{fname}', 'wb') as fileObj:
        copyfileobj(
            req.raw,
            fileObj
        )
    return f'static/a/tokens/{fname}'

def runner(l:list):

    newImgs = []
    for addr in l:

        if randint(0, 5) == 5:
            sleep(5)

        newImgs.append(
            downloader(addr)
        )
    return newImgs

def trove():

    tokens = getTokens()
    segmentsSize = round( len(tokens) / 2 )

    l1 = tokens[0: segmentsSize]
    l2 = tokens[segmentsSize + 1:]

    t1 = Thread(
        target=runner,
        args=(l1,)
    )
    t2 = Thread(
        target=runner, 
        args=(l2,)
    )

    t1.start()
    t2.start()
    print('trove has finished')
    t1.join()
    t2.join()
    return True

