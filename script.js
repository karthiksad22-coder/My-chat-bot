async function loadHistory(){

let response = await fetch("/get_history");
let history = await response.json();

let container=document.getElementById("historyList");
container.innerHTML="";

history.reverse().forEach(chatItem=>{

let row=document.createElement("div");
row.className="historyItem";

let text=document.createElement("span");
text.innerText=chatItem.user;

text.onclick=function(){
chat.innerHTML="";
addMessage(chatItem.user,"user");
addMessage(chatItem.bot,"bot");
};

let dots=document.createElement("span");
dots.innerText="⋮";
dots.className="menuBtn";

dots.onclick=function(e){

e.stopPropagation();

let menu=document.createElement("div");
menu.className="dropdownMenu";

menu.innerHTML=`
<div class="share">Share</div>
<div class="group">Start a group chat</div>
<div class="rename">Rename</div>
<div class="move">Move to project</div>
<div class="pin">Pin chat</div>
<div class="archive">Archive</div>
<div class="delete" style="color:red">Delete</div>
`;

document.body.appendChild(menu);

let rect=e.target.getBoundingClientRect();
menu.style.left=rect.left+"px";
menu.style.top=(rect.bottom+5)+"px";

/* DELETE */
menu.querySelector(".delete").onclick=async ()=>{
await fetch("/delete_chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({id:chatItem.id})
});
menu.remove();
loadHistory();
};

/* RENAME */
menu.querySelector(".rename").onclick=async ()=>{
let newName=prompt("Rename chat:");
if(!newName) return;

await fetch("/rename_chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({id:chatItem.id,name:newName})
});
menu.remove();
loadHistory();
};

/* PIN */
menu.querySelector(".pin").onclick=async ()=>{
await fetch("/pin_chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({id:chatItem.id})
});
menu.remove();
loadHistory();
};

/* ARCHIVE */
menu.querySelector(".archive").onclick=async ()=>{
await fetch("/archive_chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({id:chatItem.id})
});
menu.remove();
loadHistory();
};

/* SHARE */
menu.querySelector(".share").onclick=async ()=>{
let res = await fetch("/share_chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({id:chatItem.id})
});

let data = await res.json();
prompt("Share this link:",data.link);
};

/* GROUP CHAT */
menu.querySelector(".group").onclick=()=>{
alert("Group chat feature coming soon.");
};

/* MOVE TO PROJECT */
menu.querySelector(".move").onclick=()=>{
alert("Move to project feature coming soon.");
};

document.addEventListener("click",()=>menu.remove(),{once:true});

};

row.appendChild(text);
row.appendChild(dots);
container.appendChild(row);

});
}