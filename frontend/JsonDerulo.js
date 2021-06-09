function getMain () {
    return fetch('response_1623132079225.json')
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

getMain().then(response => {
    return response.json();
}).then(response => {
    updateRound(response);
    updatePlayers(response);
}).catch(error => {
    console.log(error)
})