var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
     console.log("Connecté à la socket flask")
});

function createServer(){
    console.log("yo21")
    let allserver = '{{server["name"]}}';
    console.log(allserver);
    var ele = document.getElementById("Serveurs");
}

document.querySelector('#start').addEventListener('click', function (e) { 
    navigator.getUserMedia({
        video : false,
        audio : true 
    }, function (stream) {
        let p = new SimplePeer({
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
})