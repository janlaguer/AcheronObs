var ws = new WebSocket(`ws://localhost:8000/ws/winner`);

ws.onmessage = event => {
    console.log(event)
}