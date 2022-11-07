var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
var recognition = new SpeechRecognition();
var labelContent = '';
recognition.continuous = true; 

recognition.onresult = function(event) {

    var curInd = event.resultIndex;
    var transcript = event.results[curInd][0].transcript;

    labelContent += transcript;
    document.getElementById("label").value = labelContent;
};

recognition.onstart = function() {
    labelContent = '';
    document.getElementById('recordingInstructions').innerText = 'Speech recognition service has started';
};

recognition.onspeechend = function() {
    document.getElementById('recordingInstructions').innerText = 'Speech has stopped being detected';
};

recognition.onerror = function(event) {
    document.getElementById('recordingInstructions').innerText = 'Speech recognition error detected';
};

function recordingStart(){
    console.log("micro started")
    recognition.start();
    document.getElementById('recordingInstructions').innerText = 'Voice recognition started.';

};

function recordingStop(){
    console.log("microphone stopped")
    recognition.stop();

    document.getElementById('recordingInstructions').innerText = 'Voice recognition paused.';
};
