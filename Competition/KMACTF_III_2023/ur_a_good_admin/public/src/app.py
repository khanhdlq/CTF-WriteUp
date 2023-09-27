from flask import Flask, session, request, redirect, render_template
from base64 import b64decode, b64encode
import base64
import pickle
from config import config
app = Flask(__name__)
#key: QhJg4gLABW7JY7mcnmoGOpUpO4iOlRYRU7ZrE33Gr8FWPn5f60V4c3GM2CFrws
app.config['SECRET_KEY'] = config.secret_key()

@app.route('/')
def home():
    if not session.get('user'):
        return redirect('/login')
    return redirect('/admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':        
        u = request.form['username']
        p = request.form['password']
        session['user'] = u

        encoded_bytes = base64.b64encode(p.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        session['data'] = encoded_string
            
        return f"Hello {session.get('user')}" + f"Data {session.get('data')}"
        return "dude, i don't know u"

@app.route('/file')
def file():
    f = request.args.get('f')
    path = './static/'+f
    if f.endswith('py'):
        return 'Nuuu'
    if 'Python script' in config.check_mime(path):
        return 'Nuuu'
    fo = open('./static/'+f, 'rb')
    return b64encode(fo.read())

@app.route('/admin')
def admin():
    if session.get('user') == "kcsc_member":
        try:
            data = b64decode(session.get('data'))
            print(data)
            if b'R' in data or b'.' in data:
                return 'lmao_data'
            if len(data) > 32:
                return 'data so long'
            pickle.loads(data)
            return 'oki'
        except:
            return 'lmao'
    else:
        return "dude, u are not mai fen"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=False)
