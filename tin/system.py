from logging import root
from os import walk, path

def getlogfile():

    robj = []
    fObj = open('log.log', 'r')
    for line in fObj.readlines():
        x = line.split(':')

        robj.append({
            'class': x[0].lower(),
            'text': line
        })
        pass

    fObj.close()

    return robj

def getAssets():
    paths = []

    for root, dirs, files in walk('static/a/'):
        for name in files:
            paths.append(
                path.join(root, name)
            )

    return paths

