function getMain () {
    return fetch('http://localhost:8000/api/match/get_match')
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
            
            var ult = document.getElementById(`t${x}p${i}ult`)

            if (json.teams[x].players[i].ultimate_up && ult.classList.contains('ult_not')){
                ult.classList.remove('ult_not')
                ult.classList.add("ult_yes")
            }
            else if(!json.teams[x].players[i].ultimate_up && ult.classList.contains('ult_yes')){
                ult.classList.remove('ult_yes')
                ult.classList.add("ult_not")
            }
        }
    }
}

function updateLogo(json) {
    for (var x = 0; x<2; x++) {
        if (x == 0) {
            i = 'l'
        } else {
            i = 'r'
        }
        document.getElementById(`${i}teamlogo`).src = `static/teamlogos/${json.teams[x].logo}`
        // document.getElementById(`${i}teambg`).src = `static/teamlogos/${json.teams[x].logo}`
    }
}

function updateTeamName(json) {
    document.getElementById(`team0_name`).innerHTML = json.teams[0].short_name.toUpperCase()
    document.getElementById(`team1_name`).innerHTML = json.teams[1].short_name.toUpperCase()
}

function updateRound(json) {
    const num1 = parseInt(json.teams[0].game_score, 10)
    const num2 = parseInt(json.teams[1].game_score, 10)
    document.getElementById('team0_score').innerHTML = num1
    document.getElementById('team1_score').innerHTML = num2
    document.getElementById('roundCount').innerHTML = `ROUND ${num1 + num2 + 1}`

    if (json.teams[0].id == 1) {
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

function updatePreRound(json) {
    if (json.id == 1) {
        document.querySelector('#leftboxes').style.left = "-50em"
        document.querySelector('#rightboxes').style.right = "-50em"
    } else {
        document.querySelector('#leftboxes').style.left = "0em"
        document.querySelector('#rightboxes').style.right = "0em"
    }
}

function mainLoop() {
    getMain().then(response => {
        return response.json();
    }).then(response => {
        updateTeamName(response)
        updateLogo(response);
        updatePreRound(response);
        updateRound(response);
        updateSpike(response);
        updatePlayers(response);
    }).catch(error => {
        console.log(error)
    })
}

var main = setInterval(mainLoop, 1000)