from flask.globals import request
from peewee import IntegrityError
from maptin.data.virualtokens import VirtualToken as VirtualTokenDatabaseTable
from maptin.utills.http import success, fail
from maptin.exception import MaptinException

class VirtualTokens:

    def __init__(self):
        self.data = VirtualTokenDatabaseTable()

    def main(self, req: request):
        if req.method == 'POST':
            return self.POST(req.get_json())

        if req.method == 'PUT':
            return self.PUT(req.get_json())

        if req.method == 'DELETE':
            return self.DELETE(req.get_json())

    
    def POST(self, json: dict):

        if 'hex' not in json.keys():
            return fail('hex key not found.')

        if 'src' not in json.key():
            return fail('src key not found')
        
        self.data.create(json['src'], json['hex'])
        return success()

    def PUT(self, json: dict):
        
        if 'hex' not in json.keys():
            return fail('hex key not found')

        if 'x' not in json.keys():
            return fail('x key not found')

        if 'y' not in json.keys():
            return fail('y key not found')

        self.data.updateByHex(self, json['hex'], json['x'], json['y'])
        return success()

    def DELETE(self, json: dict):

        if 'hex' not in json.keys():
            return fail('hex key not found')

        self.data.deleteByHex(json['hex'])
        return success()