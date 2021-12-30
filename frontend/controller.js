var ws = new WebSocket(`ws://localhost:8000/ws/controller`);

ws.onmessage = (event) => {
    data = JSON.parse(event.data)
    console.log(data)
    let check = document.getElementById('currentstate');
    if (data.preround == 0) {
        check.textContent = "Currently, the round is playing out";
    } else if (data.preround == 1) {
        check.textContent = "Currently, it's preround";
    };
    if (data.Teams) {
        document.getElementById('sendTeam1WinEvent').value = data.Teams[0];
        document.getElementById('sendTeam2WinEvent').value = data.Teams[1];

    }
}

let togglePreround = () => {
    ws.send(JSON.stringify({'event':'togglePreround'}))
}

let sendWinEvent = (winner) => {
    let data = {
        'event':'winEvent',
        'winner':winner
    }
    ws.send(JSON.stringify(data))
}