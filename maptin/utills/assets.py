from os.path import join
from os import listdir
from .credentals import Credentials

class Assets:

    def tokens(self):

        creds = Credentials().read()

        localPath = 'static/a/tokens/'
        imgs = []
        path = join(creds['root'], localPath)
        for img in listdir(path):
            thing = join(localPath, img)
            imgs.append(thing)

        return imgs

    def maps(self):
        creds = Credentials().read()

        localPath = 'static/a/maps/'
        imgs = []
        path = join(creds['root'], localPath)
        for img in listdir(path):
            thing = join(localPath, img)
            imgs.append(thing)

        return imgs