var ws = new WebSocket(`ws://localhost:8000/ws`);
let button = document.getElementById('togglePreround');

ws.onmessage = (event) => {
    data = parseInt(JSON.parse(event.data).preround)
    let check = document.getElementById('currentstate');
    if (data == 0) {
        check.textContent = "Currently, the round is playing out";
    } else {
        check.textContent = "Currently, it's preround";
    };
}

let togglePreround = () => {
    ws.send('Button Clicked')
}