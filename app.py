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
def map_single():
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


@app.route('/')
@app.route('/dashboard/')
def index():
    return render_template('base.html')

@app.route('/map/<hex>')
def map_page(hex):
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)