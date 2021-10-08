from flask import Flask, render_template
import sqlite3



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
   
    resp = make_response(render_template('home_user.html'))
    resp.set_cookie('userID', user)
    return resp

#PAGE PRINCIPALE DE L'UTILISATEUR
@app.route('/home', methods=['GET'])
def URL_home():
    return render_template('home.html')