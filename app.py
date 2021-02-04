from json import dumps
from tin.map import createMap, updateByHex

from flask import Flask
from flask import render_template
from flask import request

from tin import authUser
from tin import createUser
from tin import keyExists
from tin import listMaps
from tin import deleteMap
from tin import getByHex
from tin import tokensList
from tin import mapsList
from tin import createToken

app = Flask(__name__)

@app.route('/ajax/user', methods=['POST'])
def ajaxuser():
    creds = request.get_json()
    if creds['type'] == 'test':
        resp = authUser(creds['uname'], creds['pword'])
        return dumps(resp)
    
    if creds['type'] == 'create':
        resp = createUser(
            creds['uname'],
            creds['pword']
        )
        return dumps(resp)

@app.route('/ajax/user/key', methods=['POST'])
def ajaxTestKey():
    key = request.get_json()
    key = key['key']
    return dumps(keyExists(key=key))

@app.route('/ajax/maps', methods=['GET', 'POST', 'DELETE'])
def maps():
    key = request.headers.get('Userkey')
    if request.method == 'GET': # get all maps that a user key has
        return dumps(listMaps(key))
    if request.method == 'POST': # create a blank map
        return dumps(createMap(key))
    if request.method == 'DELETE': # delete a map
        mapHex = request.get_json()
        return dumps(deleteMap(hex=mapHex['map'], key=key))
        
@app.route('/ajax/map', methods=['GET', 'PUT'])
def mapSingle():
    if request.method == 'GET':
        hex = request.headers.get('map')
        return dumps(getByHex(hex))
    if request.method == 'PUT': # needs to be confimed by userkey
        key = request.headers.get('Userkey')
        json = request.get_json()
        obj = dumps(updateByHex(
            hex=json['hex'],
            title=json['title'], 
            map=json['map'],
            sound=json['soundtrack'],
            usrKey=key
        ))
        return obj

@app.route('/ajax/assets/<sub_path>')
def ajaxAssets(sub_path):
    if sub_path == 'tokens':
        return dumps(tokensList())
    if sub_path == 'maps':
        return dumps(mapsList())

    return dumps({'succs': False})

@app.route('/ajax/tokens', methods=['POST'])
def ajaxTokens():
    if request.method == 'POST':
        json = request.get_json()
        return dumps(
            createToken(
                json['hex'],
                json['src'],
                0,
                0,
            )
        )

@app.route('/')
@app.route('/dashboard/')
def index():
    return render_template('base.html')

@app.route('/map/<hex>')
def map_page(hex):
    return render_template('base.html')

@app.route('/sys/<action>')
def sys(action):
    rObj = {}
    if action == 'downloadassets':
        rObj['downloadassets'] = trove()
    return dumps(rObj)

if __name__ == '__main__':
    app.run(debug=True)