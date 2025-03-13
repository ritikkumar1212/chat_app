from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI WebSocket Chat</title>
</head>
<body>
    <h1 id="chat-title">Name</h1>
    <div id="chat"></div>
    <div id="username-container">
        <input type="text" id="username" placeholder="Enter your name">
        <button onclick="setUsername()">Set Name</button>
    </div>
    <input type="text" id="message" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const socket = new WebSocket('ws://localhost:8000/ws'); // Matches FastAPI endpoint
        let username = "";

        socket.onopen = function () {
            console.log('Connected to WebSocket server');
        };

        socket.onmessage = function (event) {
            const chatDiv = document.getElementById('chat');
            const message = document.createElement('p');
            message.textContent = event.data;
            chatDiv.appendChild(message);
        };

        socket.onclose = function () {
            console.log('Disconnected from WebSocket server');
        };

        function setUsername() {
            const userInput = document.getElementById('username');
            username = userInput.value.trim() || "Anonymous";
            document.getElementById('chat-title').textContent = `${username}`;
            document.getElementById('username-container').style.display = 'none';
        }

        function sendMessage() {
            const messageInput = document.getElementById('message');

            if (!username) {
                alert("Please set your name first.");
                return;
            }

            if (messageInput.value.trim()) {
                socket.send(`${username}: ${messageInput.value}`);
                messageInput.value = '';
            }
        }
    </script>
</body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

websocket_list = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if websocket not in websocket_list:
        websocket_list.append(websocket)
    while True:
        data = await websocket.receive_text()
        for web in websocket_list:
            await web.send_text(f"{data}")