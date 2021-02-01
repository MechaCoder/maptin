from json import dumps
from tin.map import createMap

from flask import Flask
from flask import render_template
from flask import request

from tin import authUser
from tin import createUser
from tin import keyExists
from tin import listMaps

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

@app.route('/ajax/maps', methods=['GET', 'POST'])
def maps():
    key = request.headers.get('Userkey')
    if request.method == 'GET': # get all maps that a user key has
        return dumps(listMaps(key))
    if request.method == 'POST':
        return dumps(createMap(key))
@app.route('/')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)