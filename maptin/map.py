from maptin.data.exceptions import DataInvaild, DoseNotExist
from os.path import expanduser
from maptin.utills.http import fail, success
from flask.globals import request
from peewee import IntegrityError

from maptin.data.maps import Map as MapDatabaseTable
from maptin.data.userKeys import UserTokens
from maptin.data.virualtokens import VirtualToken

class Maps:

    def __init__(self):
        self.data = MapDatabaseTable()

    def main(self, req: request):
        key = req.headers.get('UserKey')
        obj = UserTokens().getIdByKey(key)
        if len(obj) != 1:
            return fail('key is invaild')
        
        if request.method == 'POST':
            return self.POST(obj[0]) #  creates blank map
        
        if request.method == 'GET':
            return self.GET(obj[0])
        
        if request.method == 'DELETE':
            json = req.get_json()
            if 'map' not in json.keys():
                return fail('map is not in request object')
            return self.DELETE(json['map'])


    def POST(self, owner_id: str):
        """ creates a blank map"""
        try:
            new_hex = self.data.create(
                owner_id=owner_id,
                map_background='/static/world-map.gif',
                map_soundtrack='https://www.youtube.com/watch?v=bANjQqUVgvM'
            )

            return success({'hex': new_hex})
        except DataInvaild as error:
            return fail(str(error))

    def GET(self, owner_id: int):
        """ gets list of maps by the owner_id """

        maps = self.data.readByOwnerId(owner_id=owner_id)
        return success({'maps': maps})

    def DELETE(self, hex:str):
        """ deletes a map """
        self.data.deleteByHex(hex=hex)
        return success()
        

class Map:

    def __init__(self):
        self.data = MapDatabaseTable()

    def main(self, req: request):

        if req.method == 'GET':
            return self.GET(req.headers.get('map'))
        if req.method == 'PUT':
            return self.PUT(
                req.headers.get('Userkey'),
                req.get_json()
            )
        if req.method == 'POST':
            return self.POST(
                req.headers.get('Userkey'),
                req.get_json()
            )
        return fail()

    def GET(self, hex: str):
        r_object = fail()
        try:
            row = self.data.readByHex(hex)[0]
            row['tokens'] = VirtualToken().getByMaphex(hex)
            r_object = success({'map': row})

        except DoseNotExist as err:
            r_object = fail(f'hex {hex} dose not exist.')

        return r_object

    def PUT(self, userKey: str, json: dict):

        if 'hex' not in json.keys():
            return fail('key hex not found')
        if 'title' not in json.keys():
            return fail('key title not found')
        if 'map' not in json.keys():
            return fail('key map not found')
        if 'soundtrack' not in json.keys():
            return fail('key width not found')
        if 'width' not in json.keys():
            return fail('key not found')
        if 'fogOfWar' not in json.keys():
            return fail('key fogOfWar not found')

        #check the userkey uid == onwer id
        obj = UserTokens().getIdByKey(userKey)
        if len(obj) != 1:
            return fail('key is invaild')

        try:
            mapData = self.data.readByHex(json['hex'])
        except DoseNotExist as err:
            return fail(err)

        if mapData[0]['owner_id'] != obj[0]:
            return fail('owner id mismatch')

        try:
            self.data.updateByHex(
                json['hex'],
                json['title'],
                json['map'],
                json['soundtrack'],
                json['width'],
                json['fogOfWar']
            )
        except DoseNotExist as err:
            return fail('the map dose not exist')
        except DataInvaild as err:
            return fail(err)
        return success()

    def POST(self, userKey: str, json: dict):
        """ updates the background """

        obj = UserTokens().getIdByKey(userKey)
        if len(obj) != 1:
            return fail('key is invaild')
        
        if 'hex' not in json.keys():
            return fail('key hex not found')

        if 'src' not in json.keys():
            return fail('key src not found')

        self.data.updateBgByHex(
            hex=json['hex'],
            bg=json['src']
        )
        return success()
