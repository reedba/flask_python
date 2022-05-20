
let likes = document.querySelector("#likes")
let num = 0;

function add(element){
    num++;
    likes.innerText = num + "likes";
}