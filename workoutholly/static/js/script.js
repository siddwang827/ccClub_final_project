/* ==========================================================
	Timer 
========================================================== */

counter = getByClass("clock__counter").childNodes[0];
roundCounter = getByClass("clock__round-counter").childNodes[0];

function start() {
	// disable input fields + start button
	inputDisabled(true);

	// save fields values
	roundLength = getByID("input_round").value;
	pauseLength = getByID("input_pause").value;
	roundNumber = getByID("input_cycles").value;

	cyclesCounter = roundNumber;
	roundNumberCurrent = 1;

	// initial start
	startCycle();
	playSound(1);

	function startCycle() {
		// set the round counter
		setRoundCounter();
		// decrease cycles counter
		cyclesCounter--;
		// start 1sec timer
		timer = setInterval(function(){
			// start round
			countDownRound();

			if ( roundLength < -1 ) {
				// start pause
				if ( pauseLength == getByID("input_pause").value ) {
					playSound(2);
				}
				countDownPause();
				if ( pauseLength < 0 ) {
					clearInterval(timer);
					playSound(1);
					roundLength = getByID("input_round").value;
					pauseLength = getByID("input_pause").value;
					if ( cyclesCounter > 0 ) {
						startCycle();
					}
				}
			}
		},1000);
	}
}

function stop() {
	clearInterval(timer);
	inputDisabled(false);
}

/* --------- Timer helper --------- */

function countDownRound() {
	counter.replaceData(0,counter.nodeValue.length,roundLength);
	roundLength--;
}

function countDownPause() {
	counter.replaceData(0,counter.nodeValue.length,pauseLength);
	pauseLength--;
}

function inputDisabled(status) {
	getByID("input_round").disabled = status;
	getByID("input_pause").disabled = status;
	getByID("input_cycles").disabled = status;
	getByClass("controller__button-start").disabled = status;
}

getByID("input_cycles").addEventListener("change", updateRoundCounter);

function updateRoundCounter() {
	roundCounter.replaceData(0,roundCounter.nodeValue.length,"0/"+getByID("input_cycles").value);
}

function setRoundCounter() {
	roundCounter.replaceData(0,roundCounter.nodeValue.length,roundNumberCurrent+"/"+roundNumber);
	roundNumberCurrent++;
}

function playSound(number){   
	var sound = new Audio("http://webdev-workout.nilswe.com/sound/beep.wav");
	
	if (number == undefined) {
		playSoundLoop();
	} else {
		var counter = number;
		var interval = setInterval(function(){
			if(counter > 0){
				playSoundLoop();
			}
			else{
				clearInterval(interval);
			}
			counter--;
		},250);
	}

	function playSoundLoop() {
		sound.play();
	}
}

/* ==========================================================
	Helper
========================================================== */

function getByClass(node) {
	return document.getElementsByClassName(node)[0];
}

function getByID(node) {
	return document.getElementById(node);
}

$(document).ready(function(){
			$('.btn').on('click',function(){
// 1.簡單測試抓到資料功能
				// $.ajax({
				// url:'https://ruienyuski.github.io/git_test/data222.json',
				// 	success:function(response){
				// 		$('.info').html('抓到資料囉!');
				// 	},
				// 	error:function(xhr){
				// 		  alert("發生錯誤: " + xhr.status + " " + xhr.statusText);
				// 	}
				// });

//2.顯示json 在網頁上
$.ajax({ 
    type: 'GET', 
    url: '', 
    dataType: 'json',
    success: function (response) { 
        $.each(response, function(index, element) {
          
        });
    },
    error:function(xhr){
		alert("發生錯誤: " + xhr.status + " " + xhr.statusText);
		}
});

			});
		});