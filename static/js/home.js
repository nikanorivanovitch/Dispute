function test()
{
    console.log("test");
}

function create_server()
{
    var server_name = document.getElementById("creation_server_name").value;
    var payload = {
        "servername" : server_name
    };

    dispute_post("/create_server", payload);
}

function rename_server(server_id)
{
    var new_server_name = document.getElementById("server_name_" + server_id.toString()).value;
    var payload = {
        "server_id" : server_id.toString(),
        "server_name" : new_server_name
    };

    dispute_post("/rename_server", payload);
}

function dispute_post(api_target, api_payload)
{
    var xhr = new XMLHttpRequest();
    xhr.open("POST", api_target, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(api_payload));
}

function remove_server(server_id)
{
    var payload = {
        "server_id" : server_id
    };

    dispute_post("/remove_server", payload);
}

function create_channel(server_id)
{
    var channel_name = document.getElementById("creation_channel_name_" + server_id.toString()).value
    var payload = {
        "server_id" : server_id,
        "channel_name" : channel_name
    };

    dispute_post("/create_channel", payload);
}

function rename_channel(channel_id)
{
    var channel_name = document.getElementById("channel_name_" + channel_id.toString()).value
    var payload = {
        "channel_id" : channel_id,
        "channel_name" : channel_name
    };

    dispute_post("/rename_channel", payload);
}

function remove_channel(channel_id)
{
    var payload = {
        "channel_id" : channel_id
    };

    dispute_post("/remove_channel", payload);
}

function search_friend()
{
    var friend_name = document.getElementById("friend_search_name").value;
    var friend_discriminant = document.getElementById("friend_search_discriminant").value;

    var payload = {
        "friend_name" : friend_name,
        "friend_discriminant" : friend_discriminant
    };

    dispute_post("/search_friend", payload);
}

function post_message(channel_id)
{
    var content = document.getElementById("new_message_content_channel_" + channel_id.toString()).value;
    var payload = {
        "channel_id" : channel_id,
        "content" : content,
    };

    document.getElementById("new_message_content_channel_" + channel_id.toString()).value = "";

    dispute_post("/post_message", payload);
}

function request_addfriend(friend_id)
{
    var payload = {
        "friend_id" : friend_id
    }

    dispute_post("/request_addfriend", payload)

    var Suggestion = document.getElementById("friend_suggestion_" + friend_id.toString());
    Suggestion.remove();

}

function accept_friend(friend_id)
{
    var payload = {
        "friend_id" : friend_id
    }

    dispute_post("/accept_friend", payload)
}

function server_tab_clicked(server_id)
{
    console.log("server clicked : ",server_id);

    hide_all_tabs()

    document.getElementById("server_main_" + server_id.toString()).hidden=false
}

function hide_all_tabs()
{
    var ThingsToHide = $("div[id^='server_main_']");

    for (var i = 0; i < ThingsToHide.length; i++) {
        ThingsToHide[i].hidden=true
    }

    var ElementToFind=document.getElementById("server_creation_form")
    ElementToFind.hidden=true

    var ElementToFind=document.getElementById("friend_list")
    ElementToFind.hidden=true

    var ElementToFind=document.getElementById("search_friend_form")
    ElementToFind.hidden=true

    var ElementToFind=document.getElementById("friend_request_list")
    ElementToFind.hidden=true

    var ElementToFind=document.getElementById("change_profilepicture_form")
    ElementToFind.hidden=true
}

function display_server_creation_form()
{
    hide_all_tabs()

    var ElementToFind=document.getElementById("server_creation_form")
    ElementToFind.hidden=false
}

function display_friend_window()
{
    hide_all_tabs()

    var ElementToFind=document.getElementById("friend_list")
    ElementToFind.hidden=false

    var ElementToFind=document.getElementById("search_friend_form")
    ElementToFind.hidden=false

    var ElementToFind=document.getElementById("friend_request_list")
    ElementToFind.hidden=false
}

function channel_tab_clicked(channel_id)
{
    console.log("channel clicked : " + channel_id.toString())
    hide_all_channels_tabs();
    document.getElementById("channel_body_" + channel_id.toString()).hidden=false
}

function add_channel_form_clicked(server_id)
{
    hide_all_channels_tabs();
    document.getElementById("creation_channel_form_" + server_id.toString()).hidden=false

    document.getElementById("configuration_server_" + server_id.toString()).hidden=false
}

function hide_all_channels_tabs()
{
    var ThingsToHide = $("div[id^='channel_body_']");

    for (var i = 0; i < ThingsToHide.length; i++) {
        ThingsToHide[i].hidden=true
    }

    var ThingsToHide = $("div[id^='creation_channel_form_']");

    for (var i = 0; i < ThingsToHide.length; i++) {
        ThingsToHide[i].hidden=true
    }

    var ThingsToHide = $("div[id^='configuration_server_']");

    for (var i = 0; i < ThingsToHide.length; i++) {
        ThingsToHide[i].hidden=true
    }
}

var socket = io();

    socket.on('connect', function() {
        socket.emit('connected');
    });

    socket.on('test', function() {
        console.log('TEST')
    });

    socket.on('new_message', function(data) {

        console.log('new message : ',data);

        var new_message = document.createElement("div");
        new_message.setAttribute("class","div_message");
        var channel_box = document.getElementById("channel_message_box_" + data["channel"].toString());

        var div_image = document.createElement("div");
        div_image.setAttribute("class","div_message_profile_picture");
        var image = document.createElement("img");
        image.setAttribute("src", "/file/" + data['emiter_image']);
        image.setAttribute("class", "message_profile_picture");

        var div_timestamp = document.createElement("div");
        div_timestamp.setAttribute("class","div_message_timestamp");
        var timestamp = document.createElement("p");
        timestamp.innerHTML = data["timestamp"];
        timestamp.setAttribute("class","message_timestamp")

        var div_name = document.createElement("div");
        div_name.setAttribute("class","div_message_user_name")
        var name = document.createElement("p");
        name.innerHTML = data["emiter_name"];
        name.setAttribute("class","message_user_name")

        var div_content = document.createElement("div")
        div_content.setAttribute("class","div_message_content");
        var content = document.createElement("p");
        content.innerHTML = data["content"];
        content.setAttribute("class","message_content");

        var line_div = document.createElement("div");

        div_image.appendChild(image);
        div_name.appendChild(name);
        div_timestamp.appendChild(timestamp);
        div_content.appendChild(content);

        line_div.appendChild(div_image);
        line_div.appendChild(div_name);
        line_div.appendChild(div_timestamp);

        new_message.appendChild(line_div);
        new_message.appendChild(div_content);

        channel_box.appendChild(new_message)
    });

    socket.on('new_channel', function(data) {

        console.log('new channel : ',data);

        // AJOUT DU CHANNEL DANS LA LISTE DES CHANNELS

        var Parent = document.getElementById("channel_list_" + data["server_id"].toString())
        var ParaToAdd = document.createElement("p")
        var DivToAdd = document.createElement("div")

        DivToAdd.setAttribute("id","div_channel_list_" + data["channel_id"].toString())
        DivToAdd.setAttribute("class","div_channel_list")
        DivToAdd.setAttribute("onclick","channel_tab_clicked(" + data["channel_id"] + ")")

        ParaToAdd.setAttribute("id","div_channel_name_list_" + data["channel_id"].toString())
        ParaToAdd.setAttribute("class","div_channel_name_list")
        ParaToAdd.innerHTML='#'+data["channel_name"].toString()

        DivToAdd.appendChild(ParaToAdd)

        Parent.appendChild(DivToAdd)

        // AJOUT DU CORPS DE CHANNEL ENTIER

        var channel_container = document.getElementById("channel_container_" + data["server_id"].toString())

        var channel_body = document.createElement("div")
        channel_body.setAttribute("id","channel_body_" + data["channel_id"].toString())
        channel_body.setAttribute("channel_id",data["channel_id"])
        channel_body.setAttribute("server_id",data["server_id"])

        // DIV UPPER = NOM MODIFIABLE DU SALON

        var div_upper = document.createElement("div")
        div_upper.setAttribute("class","div_upper")

        var nom_modifiable = document.createElement("input")
        nom_modifiable.setAttribute("id","channel_name_" + data["channel_id"])
        nom_modifiable.setAttribute("type","texte")
        nom_modifiable.setAttribute("value",data["channel_name"])
        nom_modifiable.setAttribute("class","channel_editable_label")

        var remove_button = document.createElement("input")
        remove_button.setAttribute("value","-")
        remove_button.setAttribute("type","button")
        remove_button.setAttribute("onclick","remove_channel(" + data["channel_id"] + ")")
        remove_button.setAttribute("class","channel_remove_button")

        div_upper.appendChild(nom_modifiable)
        div_upper.appendChild(remove_button)

        // RESTE

        var channel_message_body = document.createElement("div")
        channel_message_body.setAttribute("id","channel_message_body_" + data["channel_id"].toString())
        channel_message_body.setAttribute("class","generic_remain")

        var channel_message_box = document.createElement("div")
        channel_message_box.setAttribute("id","channel_message_box_" + data["channel_id"])
        channel_message_box.setAttribute("class","message_box")

        for (var i = 0; i < data["last_messages"].length; i++) {
            data["last_messages"][i]
        }

        var sending_box = document.createElement("div")
        sending_box.setAttribute("class","message_sending_box")

        var new_message_content = document.createElement("input")
        new_message_content.setAttribute("id","new_message_content_channel_" + data["channel_id"])
        new_message_content.setAttribute("type","text")

        var button_send = document.createElement("input")
        button_send.setAttribute("type","button")
        button_send.setAttribute("value","Envoyer")
        button_send.setAttribute("onclick","post_message(" + data["channel_id"] + ")")
        button_send.setAttribute("class","generic_dispute_button")

        sending_box.appendChild(new_message_content)
        sending_box.appendChild(button_send)

        channel_message_body.appendChild(channel_message_box)
        channel_message_body.appendChild(sending_box)

        channel_body.appendChild(div_upper)
        channel_body.appendChild(channel_message_body)
        channel_body.setAttribute("hidden","true")

        channel_container.appendChild(channel_body)

        // SCRIPTING

        nom_modifiable.addEventListener("keyup", function(event) {
                
        if (event.keyCode === 13) {
            event.preventDefault();
            rename_channel(data["channel_id"]);
            document.activeElement.blur();

        }

        });

    });

    socket.on('rename_channel', function(data){

        console.log('rename channel : ', data);

        document.getElementById("div_channel_name_list_" + data["channel_id"].toString()).innerHTML = data["new_name"]
        document.getElementById("channel_name_" + data["channel_id"].toString()).value = data["new_name"]

    });

    socket.on('remove_channel', function(data){

        console.log('remove_channel : ', data);

        document.getElementById("channel_body_" + data["channel_id"].toString()).remove()
        document.getElementById("div_channel_list_" + data["channel_id"].toString()).remove()

    });

    socket.on('rename_server', function(data){

        console.log('rename server : ', data);

        var name = document.getElementById("server_name_" + data["server_id"].toString())

        name.setAttribute("value",data["new_name"])

    });

    socket.on('friend_search', function(data) {

        var friend_search_list = document.getElementById("friend_search_list");

        while (friend_search_list.firstChild) {
            friend_search_list.removeChild(friend_search_list.firstChild);
        }


        console.log("DATA : ",data);
        
        for (var i = 0; i<data.length ; i++) {
            
            var friend_div = document.createElement("div");
            var friend_name_div = document.createElement("div");
            var friend_image_div = document.createElement("div");
            var friend_button_add_div = document.createElement("div");

            friend_div.setAttribute("class","div_friend_suggestion")
            friend_div.setAttribute("id","friend_suggestion_" + data[i]['id'].toString())
            friend_name_div.setAttribute("class","div_friend_suggestion_name")
            friend_image_div.setAttribute("class","div_friend_suggestion_image")
            friend_button_add_div.setAttribute("class","div_friend_suggestion_button_add")

            var friend_name = document.createElement("p");
            var friend_image = document.createElement("img");
            var friend_button_add = document.createElement("input");

            friend_name.innerHTML = data[i]["name"]
            friend_name.setAttribute("class","friend_suggestion_name")

            friend_image.setAttribute("src","/file/" + data[i]["image_token"])
            friend_image.setAttribute("class","friend_suggestion_image")

            friend_button_add.setAttribute("type","image")
            friend_button_add.setAttribute("class","friend_suggestion_button_add")
            friend_button_add.setAttribute("src","/file/add_button")
            friend_button_add.setAttribute("onclick","request_addfriend(" + data[i]['id'].toString() + ")")

            friend_name_div.appendChild(friend_name)
            friend_image_div.appendChild(friend_image)
            friend_button_add_div.appendChild(friend_button_add)

            friend_div.appendChild(friend_image_div)
            friend_div.appendChild(friend_name_div)
            friend_div.appendChild(friend_button_add_div)
            friend_search_list.appendChild(friend_div)

        }
    });

    socket.on('new_friend', function(data) {

        var friend_list = document.getElementById("real_friend_list");

        console.log(friend_list)

        console.log("new_friend : ",data);
        
        var friend_div = document.createElement("div");
        var friend_name_div = document.createElement("div");
        var friend_image_div = document.createElement("div");

        friend_div.setAttribute("class","div_friend_list")
        friend_image_div.setAttribute("class","div_friend_picture")
        friend_name_div.setAttribute("class","div_friend_name")

        var friend_name = document.createElement("p");
        var friend_image = document.createElement("img");

        friend_name.innerHTML = data["name"]
        friend_name.setAttribute("class","name_friend_list")

        friend_image.setAttribute("src","/file/" + data["picture_token"])
        friend_image.setAttribute("class","picture_friend_list")

        friend_name_div.appendChild(friend_name)
        friend_image_div.appendChild(friend_image)

        friend_div.appendChild(friend_image_div)
        friend_div.appendChild(friend_name_div)
        friend_list.appendChild(friend_div)

        document.getElementById("div_friend_request_" + data["id"].toString()).remove()
    });

    socket.on('new_friend_request', function(data) {

        var friend_request_list = document.getElementById("friend_request_list");

        console.log("new_friend_request : ",data);
        
        var friend_request_div = document.createElement("div");
        var friend_name_div = document.createElement("div");
        var friend_image_div = document.createElement("div");
        var friend_accept_div = document.createElement("div");
        var friend_deny_div = document.createElement("div");

        friend_request_div.setAttribute("class","div_friend_request")
        friend_request_div.setAttribute("id","div_friend_request_" + data["id"].toString())
        friend_image_div.setAttribute("class","div_friend_request_image")
        friend_name_div.setAttribute("class","div_friend_request_name")
        friend_accept_div.setAttribute("class","div_friend_request_button")
        friend_deny_div.setAttribute("class","div_friend_request_button")

        var friend_name = document.createElement("p");
        var friend_image = document.createElement("img");
        var friend_button = document.createElement("input")

        friend_name.innerHTML = data["name"]
        friend_name.setAttribute("class","name_friend_list")

        friend_image.setAttribute("src","/file/" + data["picture_token"])
        friend_image.setAttribute("class","friend_request_image")

        friend_button.setAttribute("type","image")
        friend_button.setAttribute("class","friend_request_button")

        var accept_button = friend_button.cloneNode(true)
        var deny_button = friend_button.cloneNode(true)

        accept_button.setAttribute("src","/file/button_accept")
        accept_button.setAttribute("onclick","accept_friend(" + data["id"].toString() + ")")

        deny_button.setAttribute("src","/file/button_deny")
        deny_button.setAttribute("onclick","deny_friend(" + data["id"].toString() + ")")

        friend_name_div.appendChild(friend_name)
        friend_image_div.appendChild(friend_image)
        friend_accept_div.appendChild(accept_button)
        friend_deny_div.appendChild(deny_button)

        friend_request_div.appendChild(friend_image_div)
        friend_request_div.appendChild(friend_name_div)
        friend_request_div.appendChild(friend_accept_div)
        friend_request_div.appendChild(friend_deny_div)

        friend_request_list.appendChild(friend_request_div)
    });

    socket.on('new_user', function(data) {

        console.log("new_user : ",data);

        var server_user_list = document.getElementById("server_user_list_" + data["server_id"].toString())

        var div_user = document.createElement("div")
        var div_name = document.createElement("div")
        var div_image = document.createElement("div")

        var user_name = document.createElement("p")
        var user_image = document.createElement("img")

        div_user.setAttribute("id","div_user_list_" + data["user_id"])
        div_user.setAttribute("class","div_user_list")

        div_image.setAttribute("class","div_user_list_picture")

        div_name.setAttribute("class","div_user_list_name")

        user_name.setAttribute("class","name_user_list")
        user_name.innerHTML = data["name"]

        user_image.setAttribute("class","picture_user_list_connected")
        user_image.setAttribute("src","/file/"+data["picture_token"])

        div_image.appendChild(user_image)
        div_name.appendChild(user_name)

        div_user.appendChild(div_image)
        div_user.appendChild(div_name)

        server_user_list.appendChild(div_user)
    });

    hide_all_tabs();
    hide_all_channels_tabs();