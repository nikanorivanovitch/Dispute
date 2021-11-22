from flask import Flask, render_template, request, make_response, redirect, url_for, session
import hashlib
from dispute_sql import *
import uuid

app = Flask(__name__, template_folder='templates')

#PAGE D'ACCUEIL
@app.route('/')
def URL_root():
    print(__file__)

    if('token' in session):
        if(sh.IsValidSession(session['token'])):

            return redirect('/home')

    return render_template('root.html')

#PAGE DE CONNEXION
@app.route('/login', methods=['GET','POST'])
def URL_login():

    if(request.method == 'POST'):

        user = User()

        user.email = request.form['email']
        user.hash = sha256(request.form['password'])

        user = db.DoesThisUserExist(user)

        print('LOGIN',user)

        if(user):
            session['username'] = user.name
            session['token'] = sh.OpenSession(user)
            return redirect('/home')

        return redirect('/login')

    if(request.method == 'GET'):

        if('token' in session):
            if(sh.IsValidSession(session['token'])):
                return redirect('/home')
        
        resp = make_response(render_template('login.html'))
        return resp

#PAGE D'INSCRIPTION
@app.route('/register', methods=['GET','POST'])
def URL_register():

    if(request.method == 'POST'):

        user = User()

        user.name = request.form['username']
        user.email = request.form['email']
        user.hash = sha256(request.form['password'])

        user = db.CreateUser(user)

        session["username"] = user.name
        session["token"] = sh.OpenSession(user)

        return redirect('/home')

    if(request.method == 'GET'):

        resp = make_response(render_template('register.html'))
        return resp

#PAGE PRINCIPALE DE L'UTILISATEUR
@app.route('/home', methods=['GET'])
def URL_home():

    print("SESSION : ",session.__dict__)
    print("token" in session)

    if("token" in session):
        if(sh.IsValidSession(session["token"])):

            attributes = {}
            user = sh.Sessions[session["token"]]

            attributes["username"] = user.name

            return render_template('home.html', attributes=attributes)

    return redirect('/')

@app.route('/create_server', methods=['POST'])
def URL_create_server():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session["token"])):

                server = Server()
                server.name = request.form['servername']
                server.creator = sh.Sessions[session['token']]

                server = db.CreateServer(server)

    return redirect('/home')

    pass

if __name__ == "__main__":

    db = DatabaseHandler("database.db")
    sh = SessionHandler()

    db.GetEntireTable("user")

    print(db.GetIncrementOfTable("user"))

    app.secret_key = 'SecretBienGardéIsseMesBonsSeigneurs'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
