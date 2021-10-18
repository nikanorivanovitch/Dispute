from flask import Flask, render_template
import hashlib
import populate_sqlite3 as db
import uuid

app = Flask(__name__, template_folder='templates')

# DO IT IN FRONT, DO NOT COMMUNICATE CLEAR PASSWORD TO SERVER
def hashText(text): #create a hash password from user clear password, src :https://gist.github.com/markito/30a9bc2afbbfd684b31986c2de305d20
    """
        Basic hashing function for a text using random unique salt.  
    """
    salt = uuid.uuid4().hex
    print(salt)
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

#PAGE D'ACCUEIL
@app.route('/')
def URL_root():
    print(__file__)
    return render_template('root.html')

#PAGE DE CONNEXION
@app.route('/login', methods=['GET','POST'])
def URL_login():
    if request.method == 'POST':
        username = request.form['username']
   
        resp = make_response(render_template('login.html'))
        resp.set_cookie('userID', user)
        return resp

#PAGE D'INSCRIPTION
@app.route('/register', methods=['GET','POST'])
def URL_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] #already hash in client
        db.auth_user(username,password)
        
   
    resp = make_response(render_template('home_user.html'))
    resp.set_cookie('userID', user)
    return resp

#PAGE PRINCIPALE DE L'UTILISATEUR
@app.route('/home', methods=['GET'])
def URL_home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
