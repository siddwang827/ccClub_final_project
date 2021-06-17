window.open('','_self','');
var otimer;
var second=3;
function timer(){
    otimer.innerHTML=second;
    if(second>0){
        second=second-1;
        return false;
    }
    window.close();
} 
window.onload=function(){
    otimer=document.getElementById("timer");
    setInterval(timer,1000);
}
           