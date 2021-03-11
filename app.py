import logging
from json import dumps, loads

from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from flask_socketio import SocketIO, emit

from maptin import *

logging.basicConfig(
    filename=Credentials().read()['log'],
    level=logging.NOTSET,
    format="%(asctime)s ::: %(levelname)s:%(name)s:%(message)s"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'socket'
socket_app = SocketIO(app)


@app.errorhandler(404)
def notfound(e):
    logging.error(e)
    return render_template('404.html')


@app.route('/ajax/user', methods=['POST'])
def ajaxuser():
    resp = fail('the type key is invaild')
    creds = request.get_json()
    if creds['type'] == 'test':
        resp = User().testUser(request)

    if creds['type'] == 'create':
        resp = User().createUser(request)
    return dumps(resp)


@app.route('/ajax/user/key', methods=['POST'])
def ajaxTestKey():
    key = request.get_json()
    key = key['key']
    return dumps(
        UserToken().checkToken(key)
    )


@app.route('/ajax/maps', methods=['GET', 'POST', 'DELETE'])
def maps():
    return Maps().main(request)


@app.route('/ajax/map', methods=['GET', 'PUT'])
def mapSingle():
    m_obj = Map()
    obj = m_obj.main(request)

    if request.method == 'PUT':
        socket_app.emit(
            'map:updated', 
            m_obj.GET(request.json()['hex'])
        )
    
    return dumps(obj)


@app.route('/ajax/map/bg', methods=['POST'])
def mapSingleBg():    
    m_obj = Map()
    obj = m_obj.main(request)
    socket_app.emit('map:updated', m_obj.GET(
        request.get_json()['hex']
    ))
    return dumps(obj)


@app.route('/ajax/assets/<sub_path>')
def ajaxAssets(sub_path):
    if sub_path == 'tokens':
        return dumps(Assets().tokens())
    if sub_path == 'maps':
        return dumps(Assets().maps())

    return dumps({'succs': False})


# @app.route('/ajax/tokens', methods=['POST'])
# def ajaxTokens():
#     if request.method == 'POST':
#         json = request.get_json()
#         obj = createToken(json['hex'], json['src'], 260, 260)
#         socket_app.emit(
#             'map:update:tokens',
#             {'tokens': vTokenData().readByMapHex(json['hex'])}
#         )
#         return dumps(obj)

@app.route('/ajax/tokens', methods=['POST'])
@app.route('/ajax/token', methods=['PUT', 'DELETE'])
def ajaxTokens():
    obj = VirtualTokens().main(request)
    return dumps(obj)

# def ajaxToken():
#     if request.method == 'PUT':
#         json = request.get_json()
#         return dumps(updateLocation(json['hex'], json['x'], json['y']))
#     if request.method == 'DELETE':  # deletes a v-token.
#         hex = request.headers.get('hex')
#         obj = removeVtoken(hex)
#         socket_app.emit('vtoken:remove', {'hex': hex})
#         return dumps(obj)


@app.route('/')
@app.route('/dashboard/')
def index():
    return render_template('base.html', pageTitle='dashboard')


@app.route('/map/<hex>')
def map_page(hex):
    obj = Map().GET(hex)
    if obj['succ'] is False:
        abort(404)
    return render_template('base.html', pageTitle='map')


# @app.route('/sys/')
# @app.route('/sys/<cmd>/<pin>')
# def sys(cmd: str = '', pin: str = ''):
#     """
#     /sys/downloadassets
#     """
#     settings = Settings()

#     if cmd == 'dla':
#         if pin != settings.get('sessionSysKey'):
#             abort(404)
#         trove()
#         settings.resetSessionSysKey()

#     if cmd == 'ut':
#         if pin != settings.get('sessionSysKey'):
#             abort(404)
#         runUnittest()
#         settings.resetSessionSysKey()

#     return render_template(
#         'system.html',
#         logStr=systems.getlogfile(),
#         files=systems.getAssets(),
#         unitTestResult=systems.getUnittest()
#     )


@socket_app.on('connect')
def connect():
    emit('new client.')


@socket_app.on('vtoken:conseal')
def consoleupdate(_data={}):
    updateConseal(_data['uhex'], _data['conseal'])

    if _data['conseal']:
        _data['conseal'] = False
    else:
        _data['conseal'] = True

    emit('vtoken:conseal', _data, broadcast=True)
    pass


@socket_app.on('message')
def message(_data={}):
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
    socket_app.run(app=app, debug=True)
