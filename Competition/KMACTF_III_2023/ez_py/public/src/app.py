from flask import Flask, request, session, jsonify, render_template_string
import json
import os
import ptvsd 
ptvsd.enable_attach(redirect_output=True)
print("Listenning for debug")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

black_list = ["__class__", "__base__", "sys", "import", "[", "]", "(" ,")" ,"config", "loader", "__globals__", "sub", "os", "app", "static", "init", "\u"]

black_list2 = ["{", "%" "read","import", "builtins", "system", "eval", "session" "open", "global","request", "_", "[", "]", "()", "\\", "\"", "'", "}", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def waf(data):
    for i in black_list:
        if i in data:
            return False
    return True

def waf2(data):
    for i in black_list2:
        if i in data:
            return False
    return True 

def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

class User():
    def __init__(self):
        self.username = ""
        self.password = ""
        pass
    def check(self, data):
        if self.username == data['username'] and self.password == data['password']:
            return True
        return False

Users = []

@app.route('/register',methods=['POST'])
def register():
    try:
        if not request.data:
            return jsonify({"error": "No data provided"}), 400
        print(request.data)
        if not waf(str(request.data)):
            return jsonify({"error": "Please don't hack me"}), 400
        data = json.loads(request.data)
        print(data)
        if "username" not in data or "password" not in data:
            return jsonify({"error": "Invalid data provided"}), 400
        for user in Users:
            if user.username == data["username"]:
                return jsonify({"error": "User has exits"})
        
        user = User()
        merge(data, user)
        Users.append(user)
        return jsonify({"message": "Register successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/login',methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        if "username" not in data or "password" not in data:
            return jsonify({"message":"Login Failed"}), 400
        for user in Users:
            if user.check(data):
                session["username"] = data["username"]
                session["isAdmin"] = False
                return jsonify({"message": "Login Success"}), 200
        return jsonify({"message": "User not found"}), 401
    except Exception:
        return jsonify({"message":"Login Failed"}), 500

@app.route('/flag', methods=['GET'])
def getflag():
    if session and session["isAdmin"] == True:
        username = session["username"]
        if not waf2(username):
            return jsonify({"message": "You are fake admin ???"})
        message = "Welcome " + username + ", you are real admin!!!"
        return render_template_string(message)
    else:
        return jsonify({"message":"You are not admin"}), 200
    
@app.route('/', methods=['GET'])
def index():
    if session and session["username"]:
        return "Hello " + session["username"]
    else:
        return "Hello guest"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)