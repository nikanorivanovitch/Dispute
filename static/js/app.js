const browserSupportsMedia = () => {
    return navigator.mediaDevices.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.mzGetUserMedia
}

console.log(attributes)
let server_button = null
// Create Serveur List
const div_serv = document.getElementById("Serveurs");
for(let i = 0; i < Object.keys(attributes['servers']).length; i++) {
    let li =  document.createElement("li");
    li.setAttribute("id", attributes['servers'][i].name);
    li.innerText = attributes['servers'][i].name;
    let button = document.createElement("button");
    button.setAttribute("id", "button-" + attributes['servers'][i].name);
    button.innerText = "Connection"
    button.addEventListener('click', StartServ())
    li.appendChild(button);
    div_serv.appendChild(li);
}


//Create Firend List
const div_friend = document.getElementById("Amis");
for(let i = 0; i < Object.keys(attributes['friends']).length; i++) {
    let li =  document.createElement("li");
    li.setAttribute("id", attributes['friends'][i].name);
    li.innerText = attributes['friends'][i].name;
    let button = document.createElement("button");
    button.setAttribute("id", "button-" + attributes['friends'][i].name);
    button.innerText = "Join serv"
    button.addEventListener('click', function (e) { JoinFriendServ(e) })
    li.appendChild(button);
    div_friend.appendChild(li);
}


// Function call when trying to join friend server
function JoinFriendServ(event){
    console.log(event)
    console.log(event["target"]["id"])
}

// ==========================================================
// Partie socket
// ==========================================================

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log("Connecté à la socket flask")
});

// ==========================================================
// Communication webRTC
// ==========================================================

let p = null

function bindEvents(p){
    p.on('error',function (err) {
        console.log('error',err);
    })

    p.on('signal',function (data) {
        document.querySelector('#offer').textContent = JSON.stringify(data)
    })

    p.on('stream', function (stream) {
        let sound = document.querySelector('#receiver-video')
        sound.src = window.URL.createObjectURL(stream)
        sound.play()
    })
}

function StartServ() {
    navigator.mediaDevices.getUserMedia({
        audio : true 
    }, function (stream) {
        p = new SimplePeer({
            initiator : true,
            stream : stream,
            rickle : false
        })
        bindEvents(p)
        let emitterVideo = document.querySelector('#emitter-video')
        emitterVideo.volume = 0 
        emitterVideo.src = window.URL.createObjectURL(stream) 
        emitterVideo.play() 
    }, function () {})
}
/*
document.querySelector('#incoming').addEventListener('submit', function (e) {
    e.preventDefault() 
    if (p == null) { 
        let p = new SimplePeer({ 
            initiator : false, 
            trickle : false 
        })
        bindEvents(p)
    } 
    p.signal(JSON.parse(e.target.querySelector('textarea').value)) 
    
})
*/