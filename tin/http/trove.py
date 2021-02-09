from os import mkdir, listdir, rmdir
from os.path import isdir, isfile
from time import sleep
from shutil import copyfileobj, rmtree
from random import randint
from threading import Thread


from requests.api import get
from .base import getObject
from tin.data.commons import mkHex

def mkFname(dest:str, oldfname:str):
    files = listdir(dest)
    fileExtention = oldfname.split('.')[-1]

    while True:
        key = mkHex(8)
        if f'{key}.{fileExtention}' not in files:
            return f'{key}.{fileExtention}'

def getTokens(addr: str):
    url = addr
    obj = getObject(url=url)

    css = '#index-holder__container table#list tbody tr td:first-child a'
    tokens_onSite = []
    for el in obj.select(css):
        
        if el.text.split('.')[-1] in ['png', 'gif', 'jpg']:
            tokens_onSite.append(
                f'{url}{ el["href"] }'
            )
    return tokens_onSite

def downloader(img_addr:str, subFolder:str = 'tokens'):

    fname = img_addr.split("/")[-1]
    req = get(img_addr, stream=True)
    req.raw.decode_content = True

    if isdir('static/a') == False:
        mkdir('static/a')
    
    if isdir(f'static/a/{subFolder}') == False:
        mkdir(f'static/a/{subFolder}')

    fname = mkFname(f'static/a/{subFolder}', fname)
    
    with open(f'static/a/{subFolder}/{fname}', 'wb') as fileObj:
        copyfileobj(
            req.raw,
            fileObj
        )
    return f'static/a/{subFolder}/{fname}'

def runner(l:list, sub:str = 'tokens'):

    rmtree(f'static/a/{sub}', ignore_errors=True)

    newImgs = []
    for addr in l:

        if randint(0, 5) == 5:
            sleep(5)

        newImgs.append(
            downloader(addr, sub)
        )
    return newImgs

def trove():

    tokens = getTokens("https://thetrove.is/Assets/By%20Artist%20or%20Source/5eTools/currated/Token/")
    tokens += getTokens("https://thetrove.is/Assets/Tokens%20(by%20View)/Overhead/All%20the%20Lights%20in%20the%20Sky%20are%20Stars%20-%20Aeyana%20%28H%29/")
    segmentsSize = round( len(tokens) / 2 )

    l1 = tokens[0: segmentsSize]
    l2 = tokens[segmentsSize + 1:]

    maps = getTokens('https://thetrove.is/Assets/By%20Artist%20or%20Source/Skyrim/')
    maps += getTokens('https://thetrove.is/Assets/Maps%20&%20Tiles/BattleMaps/City%20Based/Lost%20Mine%20of%20Phandelver%20Maps/')
    maps + getTokens('https://thetrove.is/Assets/Maps%20&%20Tiles/BattleMaps/City%20Based/Neverwinter/neverwinter_environs.jpg')

    segmentsSize = round( len(maps) / 2 )
    l3 = maps[0: segmentsSize]
    l4 = maps[segmentsSize + 1:]

    t1 = Thread(
        target=runner,
        args=(l1,)
    )
    t2 = Thread(
        target=runner, 
        args=(l2, )
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print('cooldown ten seconds')
    sleep(10)

    t3 = Thread(
        target=runner, 
        args=(l3, 'maps')
    )
    t4 = Thread(
        target=runner, 
        args=(l4, 'maps')
    )
    t3.start()
    t4.start()

    t3.join()
    t4.join()

    print('trove has finished')
    return True

