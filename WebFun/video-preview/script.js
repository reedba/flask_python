console.log("page loaded...");
var x = document.getElementById("video");

function over(element){
    x.play();
}

function out(element){
    x.pause();
    x.currentTime = 0;
}