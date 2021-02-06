from json import dumps, loads

from werkzeug import debug
from tin.data.settings import Settings
from tin.map import createMap, updateByHex

from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, emit, send
from tin.http.trove import trove

from tin import authUser
from tin import createUser
from tin import keyExists
from tin import listMaps
from tin import deleteMap
from tin import getByHex
from tin import tokensList
from tin import mapsList
from tin import createToken
from tin import updateLocation
from tin import upadateBgByHex
from tin import removeVtoken

app = Flask(__name__)
app.config['SECRET_KEY'] = Settings().get('socketKey')
socket_app = SocketIO(app)

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

@app.route('/ajax/map/bg', methods=['POST'])
def mapSingleBg():
    json = request.get_json()
    obj = upadateBgByHex(json['hex'], json['src'])
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
                100,
            )
        )

@app.route('/ajax/token', methods=['PUT', 'DELETE'])
def ajaxToken():
    if request.method == 'PUT':
        json = request.get_json()
        return dumps(updateLocation(json['hex'], json['x'], json['y']))
    if request.method == 'DELETE':
        hex = request.headers.get('hex')
        return dumps(removeVtoken(hex))

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

@socket_app.on('connect')
def connect():
    emit('new client.')
    print('NEW CLient')

@socket_app.on('message')
def message(_data = {}):
    obj = loads(_data)
    k = updateLocation(
        hex=obj['hex'],
        x=obj['x'],
        y=obj['y']
    )
    if k['succ']:
        emit('message', dumps({
                'hex': obj['hex'],
                'x': obj['x'],
                'y': obj['y']

            }), broadcast=True)

@socket_app.on('flash')
def flash():
    print('flash')
    emit('flash', broadcast=True)



if __name__ == '__main__':
    socket_app.run(
        app=app,
        debug=True
    )