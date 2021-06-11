function getMain () {
    return fetch('https://8lr09u.deta.dev/api/match/get_match/')
}

function updatePlayers(json) {
    for (var x = 0; x <2; x++) {
        for (var i = 0; i <= 4; i++) {
            // console.log(json.teams[0].players[i])
            document.getElementById(`t${x}p${i}`).innerText = json.teams[x].players[i].display_name.toUpperCase()
            document.getElementById(`t${x}p${i}hp`).innerText = json.teams[x].players[i].hp
            document.getElementById(`t${x}p${i}hpbar`).style.width = `${json.teams[x].players[i].hp}%`
        }
    }
}

function updateRound(json) {
    const num1 = parseInt(json.teams[0].game_score, 10)
    const num2 = parseInt(json.teams[1].game_score, 10)
    document.getElementById('team0_score').innerHTML = num1
    document.getElementById('team1_score').innerHTML = num2
    document.getElementById('roundCount').innerHTML = `ROUND ${num1 + num2 + 1}`
}

function spikePlanted() {
    document.querySelector('.spike').id = 'planted';
}

function spikeReset() {
    document.querySelector('div').removeAttribute('id');
}

getMain().then(response => {
    return response.json();
}).then(response => {
    updateRound(response);
    updatePlayers(response);
}).catch(error => {
    console.log(error)
})