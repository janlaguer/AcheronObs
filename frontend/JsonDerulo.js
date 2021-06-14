function getMain () {
    return fetch('http://26.227.230.60:8000/api/match/get_match')
}

function updatePlayers(json) {
    for (var x = 0; x <2; x++) {
        for (var i = 0; i <= 4; i++) {
            // console.log(json.teams[0].players[i])
            document.getElementById(`t${x}p${i}`).innerText = json.teams[x].players[i].display_name
            document.getElementById(`t${x}p${i}hp`).innerText = json.teams[x].players[i].hp
            document.getElementById(`t${x}p${i}hpbar`).style.width = `${json.teams[x].players[i].hp}%`
            document.getElementById(`t${x}p${i}agent`).src = `static/${json.teams[x].players[i].agent.charAt(0).toUpperCase()}${json.teams[x].players[i].agent.slice(1)}.png`
			
			//left team boxes
			var box
			if (x == 0){
				box = document.getElementById(`boxl${i+1}`)
			}
			else{
				box = document.getElementById(`boxr${i+1}`)
			}
			
			//if dead
			if (json.teams[x].players[i].hp == 0){
				box.classList.add("dead")
			}
			//if not deat
			else{
				box.classList.remove("dead")
			}
        }
    }
}

function updateRound(json) {
    const num1 = parseInt(json.teams[0].game_score, 10)
    const num2 = parseInt(json.teams[1].game_score, 10)
    document.getElementById('team0_score').innerHTML = num1
    document.getElementById('team1_score').innerHTML = num2
    document.getElementById('roundCount').innerHTML = `ROUND ${num1 + num2 + 1}`

    if (num1 + num2 >= 13) {
        // get bool if team0 and team1 has specific classes
        var team0HasClass = $('#team0_line').hasClass('attackers_line');
        var team1HasClass = $('#team1_line').hasClass('defenders_line');

        // change background colors
        document.querySelectorAll('.defenders').forEach(elem =>{
            elem.style.backgroundColor = '#d85d56';
        })
        document.querySelectorAll('.attackers').forEach(elem =>{
            elem.style.backgroundColor = '#5baa95';
        })

        if (!team0HasClass) {
            document.getElementById('team0_line').classList.remove("defenders_line")
            document.getElementById('team0_line').classList.add("attackers_line")
        }
        if (!team1HasClass) {
            document.getElementById('team1_line').classList.remove("attackers_line")
            document.getElementById('team1_line').classList.add("defenders_line")
        }
    } else {
        // get bool if team0 and team1 has specific classes
        var team0HasClass = $('#team0_line').hasClass('defenders_line');
        var team1HasClass = $('#team1_line').hasClass('attackers_line');

        // change background colors
        document.querySelectorAll('.defenders').forEach(elem =>{
            elem.style.backgroundColor = '#5baa95';
        })
        document.querySelectorAll('.attackers').forEach(elem =>{
            elem.style.backgroundColor = '#d85d56';
        })

        if (!team0HasClass) {
            document.getElementById('team0_line').classList.remove("attackers_line")
            document.getElementById('team0_line').classList.add("defenders_line")
        }
        if (!team1HasClass) {
            document.getElementById('team1_line').classList.remove("defenders_line")
            document.getElementById('team1_line').classList.add("attackers_line")
        }
    }
}

function updateSpike(json) {
    if (json.spike_status == true) {
        document.querySelector('.spike').id = 'planted';
        document.querySelector('.mid_box').id = 'hide_timer';
    } else {
        document.querySelector('.spike').removeAttribute('id');
        document.querySelector('.mid_box').removeAttribute('id');
    }
}

function mainLoop() {
    getMain().then(response => {
        return response.json();
    }).then(response => {
        updateRound(response);
        updateSpike(response);
        updatePlayers(response);
    }).catch(error => {
        console.log(error)
    })
}

var main = setInterval(mainLoop, 1000)