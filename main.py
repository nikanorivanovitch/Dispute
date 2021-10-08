from flask import Flask, render_template
import sqlite3
import hashlib
import populate_sqlite3 as db

app = Flask(__name__, template_folder='templates')

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
        password = request.form['password']
        key = hashlib.pbkdf2_hmac( #mots de pass hash
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
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
