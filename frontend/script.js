const BASE_URL = "http://127.0.0.1:5000";

// create user
async function createUser(){
let name=document.getElementById("name").value;
let email=document.getElementById("email").value;

let res=await fetch(BASE_URL+"/add_user",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name,email})
});

let data=await res.json();
localStorage.setItem("uid",data.user_id);
alert("Login success. User ID: "+data.user_id);
window.location="quiz.html";
}

// submit quiz
async function submitQuiz(){
let user_id=localStorage.getItem("uid");
let topic=document.getElementById("topic").value;
let score=document.getElementById("score").value;
let total=document.getElementById("total").value;

await fetch(BASE_URL+"/submit_quiz",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({user_id,topic,score,total})
});

alert("Quiz submitted");
}

// get progress
async function getProgress(){
let uid=localStorage.getItem("uid");
let res=await fetch(BASE_URL+"/progress/"+uid);
let data=await res.json();

document.getElementById("output").innerHTML=
"<b>Progress:</b><br>"+JSON.stringify(data,null,2);
}

// recommendation
async function getRecommendation(){
let uid=localStorage.getItem("uid");
let res=await fetch(BASE_URL+"/recommend/"+uid);
let data=await res.json();

document.getElementById("output").innerHTML=
"<b>Recommendation:</b><br>"+JSON.stringify(data,null,2);
}

function goDashboard(){
window.location="dashboard.html";
}

function goQuiz(){
window.location="quiz.html";
}
