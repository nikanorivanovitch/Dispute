from flask import Flask, render_template, request, make_response, redirect, url_for, session, flash, send_file
from flask_socketio import SocketIO, join_room, leave_room
from werkzeug.utils import secure_filename
import hashlib
import uuid
import time
from dispute_sql import *

UPLOAD_FOLDER = "./files/"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

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

            attributes['user'] = {'name' : user.name, 'discriminant' : user.discriminant, 'picture_token' : user.picture_token}
            attributes['pending_friend_requests'] = db.GetFriendRequestsOfUser(user.id)
            attributes['servers'] = db.GetServersOfUser(user.id)
            attributes['friends'] = db.GetFriendsOfUser(user.id)

            return render_template('home.html', attributes=attributes)

    return redirect('/')

# <API> fonctionne avec des JSON
@app.route('/create_server', methods=['POST'])
def URL_create_server():

    print(request.json)

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                server = Server()
                server.name = request.json['servername']
                server.creator = sh.Sessions[session['token']]

                server = db.CreateServer(server)

                main_channel = Channel()
                main_channel.name = "général"
                main_channel.server_id = server.id

                main_channel = db.CreateChannel(main_channel)

                socketio.emit('new_server', {'server_id' : server.id, 'server_name' : server.name, 'server_image_token' : server.picture_token, 'channels' : [{'channel_id' : main_channel.id,'channel_name' : main_channel.name}]}, room=session['token'])

    return '0'

# <API> fonctionne avec des JSON
@app.route('/rename_server', methods=['POST'])
def URL_rename_server():

    print("REQUEST")
    print(request.json)

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                server = Server()
                server.id = request.json['server_id']
                server.name = request.json['server_name']
                server.creator = sh.Sessions[session['token']]
                user = sh.Sessions[session['token']]

                if(db.IsServerAdmin(server.id, user)):
                    server = db.RenameServer(server)
                    print(db.GetUserOfServer(server.id))

                for user_id in db.GetUserOfServer(server.id):

                    token = sh.IsUserConnected(user_id)

                    if(token != False):

                        socketio.emit('rename_server', {'server_id' : server.id, 'new_name' : server.name}, room=token)




    return '0'

# <API> fonctionne avec des JSON
@app.route('/remove_server', methods=['POST'])
def URL_remove_server():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                server_id = request.json['server_id']
                user = sh.Sessions[session['token']]

                users_ids_of_server = db.GetUserOfServer(server_id)

                if(db.IsServerAdmin(server_id, user)):

                    db.RemoveServer(server_id)

                    for user_id_to_remove in users_ids_of_server:

                        token = sh.IsUserConnected(user)

                        if(token!=False):

                            socketio.emit('remove_server', {'server_id' : server_id}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/create_channel', methods=['POST'])
def URL_create_channel():

    print(request.json)

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                channel = Channel()
                channel.server_id = request.json['server_id']
                channel.name = request.json['channel_name']
                user = sh.Sessions[session['token']]

                #if(db.IsServerAdmin(channel.server_id, user)):
                db.CreateChannel(channel)

                for user_id in db.GetUserOfServer(channel.server_id):

                    token = sh.IsUserConnected(user_id)

                    if(token != False):

                        socketio.emit('new_channel', {'server_id' : channel.server_id ,'channel_id' : channel.id, 'channel_name' : channel.name, 'last_messages' : []}, room=token)

    return redirect('/home')

    pass

# <API> fonctionne avec des JSON
@app.route('/rename_channel', methods=['POST'])
def URL_rename_channel():

    print(request.json)

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                channel = Channel()
                channel.id = request.json['channel_id']
                channel.name = request.json['channel_name']
                server_id = db.GetServerOfChannel(channel.id)
                user = sh.Sessions[session['token']]

                if(db.IsChannelAdmin(channel.id, user)):
                    db.RenameChannel(channel)

                for user_id in db.GetUserOfServer(server_id):

                    token = sh.IsUserConnected(user_id)

                    if(token != False):

                        socketio.emit('rename_channel', {'channel_id' : channel.id, 'new_name' : channel.name}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/remove_channel', methods=['POST'])
def URL_remove_channel():

    print(request.json)

    print("REMOVE CHANNEL")
    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                channel_id = request.json['channel_id']
                user = sh.Sessions[session['token']]

                users_ids_of_server = db.GetUserOfServer(db.GetServerOfChannel(channel_id))

                if(db.IsChannelAdmin(channel_id, user)):
                    db.RemoveChannel(channel_id)

                    for user_id in users_ids_of_server:

                        token = sh.IsUserConnected(user_id)

                        if(token!=False):

                            socketio.emit('remove_channel', {'channel_id' : channel_id}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/post_message', methods=['POST'])
def URL_post_message():

    print("POST MESSAGE REQUEST")

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                print("POST MESSAGE VALID")
                print(request.__dict__)
                print(request.data)
                print(request.args)
                print(request.json)

                user = sh.Sessions[session['token']]

                message = Message()
                message.content = request.json['content']
                message.sender_id = user.id
                message.channel_id = request.json['channel_id']
                message.timestamp = int(time.time())

                timestamp = str(datetime.fromtimestamp(int(message.timestamp))).replace(' ','@').replace('-','/')

                if(db.IsChannelMember(message.channel_id, user) and message.content!=""):
                    
                    db.CreateMessage(message)

                    server_id = db.GetServerOfChannel(int(message.channel_id))

                    print(server_id)

                    if(server_id == False):
                        return '0'

                    users_id = db.GetUserOfServer(int(server_id))

                    print(users_id)

                    for user_id in users_id:

                        token = sh.IsUserConnected(user_id)

                        if(token != False):

                            socketio.emit('new_message', {'content' : message.content, 'emiter_name' : user.name, 'emiter_image' : user.picture_token, 'timestamp' : timestamp, 'channel' : message.channel_id}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/request_addfriend', methods=['POST'])
def URL_request_addfriend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.json['friend_id']) and not db.DoesFriendshipExists(sh.Sessions[session['token']].id, request.json["friend_id"])):
                    db.AddFriendshipRequest(sh.Sessions[session['token']].id, request.json["friend_id"])

                    requester = sh.Sessions[session['token']]

                    token = sh.IsUserConnected(request.json["friend_id"])

                    if(token != False):
                        socketio.emit('new_friend_request', {'id' : requester.id, 'name' : requester.name, 'picture_token' : requester.picture_token}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/accept_friend', methods=['POST'])
def URL_accept_friend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.DoesFriendshipRequestExists(request.json['friend_id'], sh.Sessions[session['token']].id)):
                    db.RemoveFriendshipRequest(request.json['friend_id'], sh.Sessions[session['token']].id)
                    db.AddFriendship(sh.Sessions[session['token']].id, request.json['friend_id'])

                    friend1 = sh.Sessions[session['token']]
                    friend2 = db.GetUserApparenceFromId(request.json['friend_id'])

                    token = sh.IsUserConnected(friend2['id'])
                    if(token):
                        socketio.emit('new_friend', {'id' : friend1.id, 'name' : friend1.name, 'picture_token' : friend1.picture_token}, room=token)

                    token = sh.IsUserConnected(friend1.id)
                    if(token):
                        socketio.emit('new_friend', {'id' : friend2['id'], 'name' : friend2['name'], 'picture_token' : friend2['picture_token']}, room=token)

    return '0'

# <API> fonctionne avec des JSON
@app.route('/deny_friend', methods=['POST'])
def URL_deny_friend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.form['friend_id'])):
                    db.RemoveFriendshipRequest(request.form['friend_id'], sh.Sessions[session['token']].id)

                    user_denied = sh.Sessions[session['token']].id
                    socketio.emit('deny_request', {'id' : request.form['friend_id']}, room=token)

# <API> fonctionne avec des JSON
@app.route('/remove_friend', methods=['POST'])
def URL_remove_friend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                if(db.GetUserFromId(request.form['friend_id'])):
                    db.RemoveFriendship(sh.Sessions[session['token']].id, request.form['friend_id'])

# <API> fonctionne avec des JSON
@app.route('/search_friend', methods=['POST'])
def URL_search_friend():

    if(request.method == 'POST'):
        if("token" in session):
            if(sh.IsValidSession(session['token'])):

                print("token valide")
                print(request.json)

                if(request.json["friend_name"]!="" and request.json["friend_discriminant"]!=""):

                    print("arguments valides")

                    result = db.GetPotentialFriend(sh.Sessions[session['token']].id, request.json["friend_name"], request.json["friend_discriminant"])

                    print("RESULTS")
                    print(result)

                    socketio.emit('friend_search', result, room=session["token"])

                    return '0'
    
    socketio.emit('friend_search', [])
    return '0'


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

@app.route('/join_server/<ServerToken>',methods=['GET','POST'])
def URL_join_server(ServerToken):

    if("token" in session):
        if(sh.IsValidSession(session['token'])):

            user = sh.Sessions[session['token']]

            if(db.AddUserToServerFromToken(user.id, ServerToken)):

                users_id = db.GetUserOfServerFromToken(ServerToken)

                for user_id in users_id:

                    if(user_id==user.id):
                        continue

                    token = sh.IsUserConnected(user_id)
                    if(token):
                        print("EMIT")
                        socketio.emit('new_user', {'server_id' : db.GetServerIdFromToken(ServerToken), 'name' : user.name, 'picture_token' : user.picture_token, "user_id" : user.id}, room=token)

    return redirect('/home')

@app.route('/file/<FileToken>', methods=['GET'])
def URL_file(FileToken):

    if(request.method == 'GET'):

        if(FileToken == 'default-picture'):
            return send_file('./static_pictures/' + 'clown.jpg')

        elif(FileToken == 'default-server-picture'):
            return send_file('./static_pictures/' + 'default-server-picture.png')

        elif(FileToken == 'display_new_server_form_image'):
            return send_file('./static_pictures/' + 'display_new_server_form_image.png')

        elif(FileToken == 'button_deny'):
            return send_file('./static_pictures/' + 'button_deny.png')

        elif(FileToken == 'button_accept'):
            return send_file('./static_pictures/' + 'button_accept.png')

        elif(FileToken == 'add_button'):
            return send_file('./static_pictures/' + 'add_button.png')

        elif(db.DoesTokenFileExists(FileToken)):

            print("PATH : ",app.config['UPLOAD_FOLDER'] + FileToken + db.GetExtensionOfFileToken(FileToken))
            return send_file(app.config['UPLOAD_FOLDER'] + FileToken + db.GetExtensionOfFileToken(FileToken), as_attachment=False)

        else:
            return send_file('./static_pictures/' + 'clown.jpg')

    return 0

@app.route('/user/<UserId>', methods=['GET'])
def URL_user(UserId):

    if(request.method == 'GET'):

        if('token' in session):
            if(sh.IsValidSession(session['token'])):

                UserArray = db.GetUserFromId(UserId)

                print("GET USER : ", User.__dict__)

@socketio.on('connected')
def EVENT_connected():

    if('token' in session):
        if(sh.IsValidSession(session['token'])):

            print("CONNEXION SOCKETIO : ",session['token'])

            join_room(session['token'])

@socketio.on('disconnected')
def EVENT_disconnected():

    if('token' in session):
        if(sh.IsValidSession(session['token'])):
            leave_room(session['token'])

if __name__ == "__main__":

    db = DatabaseHandler("database.db")
    sh = SessionHandler()

    db.GetEntireTable("user")

    print(db.GetIncrementOfTable("user"))

    app.secret_key = 'SecretBienGardéIsseMesBonsSeigneurs'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1000 * 1000
    socketio.run(app)
