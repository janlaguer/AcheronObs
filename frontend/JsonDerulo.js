function getMain () {
    return fetch('response_1623132079225.json')
}

function updatePlayers(json) {
    for (var x = 0; x <=2; x++) {
        for (var i = 0; i <= 4; i++) {
            // console.log(json.teams[0].players[i].id)
            document.getElementById(`t${x}p${json.teams[0].players[i].id}`).innerText = json.teams[0].players[i].display_name.toUpperCase()
        }
    }
}

function updateRound(json) {
    const num1 = parseInt(json.teams[0].game_score, 10)
    const num2 = parseInt(json.teams[1].game_score, 10)
    document.getElementById('roundCount').innerHTML = `ROUND ${num1 + num2 + 1}`
}

getMain().then(response => {
    return response.json();
}).then(response => {
    updateRound(response);
    updatePlayers(response);
})