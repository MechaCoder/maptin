import logging
from json import dumps, loads

from tin.data.settings import Settings
from tin.map import createMap, updateByHex

from flask import Flask
from flask import render_template
from flask import request
from flask import abort

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
from tin import vTokenData
import tin.system as systems
from tin.commons import runUnittest


logging.basicConfig(filename='log.log', level=logging.NOTSET, format="%(asctime)s ::: %(levelname)s:%(name)s:%(message)s")

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
        return dumps(getByHex(hex)) ## gets all server information

    if request.method == 'PUT': # needs to be confimed by userkey
        key = request.headers.get('Userkey')
        json = request.get_json()
        obj = updateByHex(
            hex=json['hex'],
            title=json['title'], 
            map=json['map'],
            sound=json['soundtrack'],
            width=json['width'],
            fog=json['fogOfWar'],
            usrKey=key
        )
        socket_app.emit('map:updated', getByHex(json['hex']))
        return dumps(obj)

@app.route('/ajax/map/bg', methods=['POST'])
def mapSingleBg():
    json = request.get_json()
    obj = upadateBgByHex(json['hex'], json['src'])
    socket_app.emit('map:updated', getByHex(json['hex']))
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
        obj = createToken(json['hex'], json['src'], 260, 0)
        socket_app.emit('map:update:tokens', {'tokens': vTokenData().readByMapHex(json['hex'])})
        return dumps(obj)


@app.route('/ajax/token', methods=['PUT', 'DELETE'])
def ajaxToken():
    if request.method == 'PUT':
        json = request.get_json()
        return dumps(updateLocation(json['hex'], json['x'], json['y']))
    if request.method == 'DELETE': # deletes a v-token.
        hex = request.headers.get('hex')
        obj = removeVtoken(hex)
        socket_app.emit('vtoken:remove', {'hex': hex})
        return dumps(obj) 

@app.route('/')
@app.route('/dashboard/')
def index():
    return render_template('base.html', pageTitle='dashboard')

@app.route('/map/<hex>')
def map_page(hex):
    return render_template('base.html', pageTitle='map')

@app.route('/sys/')
@app.route('/sys/<cmd>/<pin>')
def sys(cmd:str = '', pin: str = ''):
    """
    /sys/downloadassets
    """
    settings = Settings()
    if cmd == 'dla':
        if pin != settings.get('sessionSysKey'):
            abort(404)
        trove()
        settings.resetSessionSysKey()

    if cmd == 'ut':
        if pin != settings.get('sessionSysKey'):
            abort(404)
        runUnittest()
        settings.resetSessionSysKey()
        

    return render_template(
        'system.html', 
        logStr=systems.getlogfile(),
        files=systems.getAssets(),
        unitTestResult=systems.getUnittest()
    )

@socket_app.on('connect')
def connect():
    emit('new client.')

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

if __name__ == '__main__':
    socket_app.run(
        app=app,
        debug=True
    )