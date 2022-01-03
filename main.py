from flask import Flask, render_template, request, make_response, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
import hashlib
import uuid
from dispute_sql import *

UPLOAD_FOLDER = "./files/"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
basedir = os.path.abspath(os.path.dirname(__file__))

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
        if(sh.IsValidSession(session['token'])):

            attributes = {}
            user = sh.Sessions[session['token']]

            attributes['username'] = user.name
            attributes['userpicturetoken'] = user.picture_token
            attributes['servers'] = db.GetServersOfUser(user.id)
            attributes['friends'] = db.GetFriendsOfUser(user.id)

            return render_template('home.html', attributes=attributes)

    return redirect('/')

@app.route('/create_server', methods=['POST'])
def URL_create_server():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                server = Server()
                server.name = request.form['servername']
                server.creator = sh.Sessions[session['token']]

                server = db.CreateServer(server)

                main_channel = Channel()
                main_channel.name = "général"
                main_channel.server_id = server.id

                main_channel = db.CreateChannel(main_channel)

    return redirect('/home')

    pass

@app.route('/remove_server', methods=['POST'])
def URL_remove_server():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                server_id = request.form['server_id']
                user = sh.Sessions[session['token']]

                db.RemoveServer(server_id, user)

    return redirect('/home')

    pass

@app.route('/create_channel', methods=['POST'])
def URL_create_channel():

    return redirect('/home')

    pass

@app.route('/remove_channel',methods=['POST'])
def URL_remove_channel():

    return redirect('/home')

    pass

@app.route('/request_addfriend', methods=['POST'])
def URL_request_addfriend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.form['friend_id'])):
                    db.AddFriendshipRequest(session['token'].id, request.form['friend_id'])

@app.route('/addfriend', methods=['POST'])
def URL_addfriend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.form['friend_id'])):
                    db.AddFriendshipRequest(session['token'].id, request.form['friend_id'])

@app.route('/removefriend', methods=['POST'])
def URL_removefriend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.form['friend_id'])):
                    db.RemoveFriendship(sh.Sessions[session['token']].id, request.form['friend_id'])

@app.route('/change_profilepicture', methods=['POST'])
def URL_change_profilepicture():

    if(request.method == 'POST'):
        # check if the post request has the file part

        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                print('FILES : ',request.files)
        
                if 'profil_picture' not in request.files:
                    print('No file part')
                    return redirect('/home')
        
                file = request.files['profil_picture']
        
                if file.filename == '':
                    print('No selected file')
        
                    return redirect('/home')
        
                if file and allowed_extension(file.filename.lower(), ALLOWED_EXTENSIONS):
        
                    filetoken = NewFileToken()
        
                    while(db.DoesTokenFileExists(filetoken)):
                        filetoken = NewFileToken()
        
                    fileextension = extension_of(file.filename.lower(), ALLOWED_EXTENSIONS)
                    filename = filetoken + fileextension
                    file.save(app.config['UPLOAD_FOLDER'] + filename)
                    print("PATH : ",app.config['UPLOAD_FOLDER'] + filename)
                    db.AddTokenFile(filetoken, fileextension)

                    sh.Sessions[session['token']].picture_token = filetoken
                    db.GetEntireTable('files')

    return redirect('/home')

@app.route('/file/<FileToken>', methods=['GET'])
def URL_file(FileToken):

    if(request.method == 'GET'):

        if(FileToken == 'default-picture'):
            return send_file('./static_pictures/' + 'clown.jpg')

        if(db.DoesTokenFileExists(FileToken)):

            print("PATH : ",app.config['UPLOAD_FOLDER'] + FileToken + db.GetExtensionOfFileToken(FileToken))
            return send_file(app.config['UPLOAD_FOLDER'] + FileToken + db.GetExtensionOfFileToken(FileToken), as_attachment=False)

        return 0

    return 0






if __name__ == "__main__":

    db = DatabaseHandler("database.db")
    sh = SessionHandler()

    db.GetEntireTable("user")

    print(db.GetIncrementOfTable("user"))

    app.secret_key = 'SecretBienGardéIsseMesBonsSeigneurs'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run()
