/* ==========================================================
	Timer 
========================================================== */

function display() {
	var btn = document.getElementById("button_start");
	var input_pause = document.getElementById("input_pause");
	var clock__counter = document.getElementById("clock");
	var clock__round = document.getElementById("clock_round");
	clock__counter.innerHTML = String(parseInt(input_pause.value));//todo : data from backend
	clock__round.innerHTML = String(parseInt(clock__round.innerHTML) + 1) + '/8';//todo : data from backend
	btn.disabled="disabled";
	var timer;
	//clearInterval(timer);
	timer = window.setInterval(function(){ 
		clock__counter.innerHTML = String(parseInt(clock__counter.innerHTML) - 1); 
		if (parseInt(clock__counter.innerHTML) <= 0) {
			clock__counter.innerHTML = '0';
			btn.disabled="";
			clearInterval(timer);
		}
	}, 1000);
}

function closeWindow(){
	  window.close();
}

