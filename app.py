import json
import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# File to store the high score
SCORE_FILE = "highscore.json"

def get_highscore():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return json.load(f).get("score", 0)
    return 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Snake: Gemini Edition</title>
    <style>
        :root { --bg: #0a0a12; --accent: #00f2ff; --snake: #7000ff; }
        body { 
            background: var(--bg); color: white; font-family: 'Courier New', monospace;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; margin: 0; overflow: hidden;
        }
        .hud { width: 400px; display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 1.2rem; border-bottom: 2px solid #333; padding-bottom: 5px; }
        canvas { 
            background: #000; border: 4px solid #333; border-radius: 4px;
            box-shadow: 0 0 50px rgba(112, 0, 255, 0.2);
        }
        .msg { margin-top: 15px; color: #666; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="hud">
        <div>SCORE: <span id="score">0</span></div>
        <div>BEST: <span id="best">{{ highscore }}</span></div>
    </div>
    <canvas id="g" width="400" height="400"></canvas>
    <div class="msg">USE ARROW KEYS • DON'T HIT THE WALLS</div>

    <script>
        const canvas = document.getElementById("g");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");
        const bestEl = document.getElementById("best");

        const grid = 20;
        let count = 0;
        let score = 0;
        let highscore = {{ highscore }};
        
        let snake = {
            x: 160, y: 160, dx: grid, dy: 0,
            cells: [], maxCells: 4
        };
        let apple = { x: 320, y: 320 };

        // Input Buffer to prevent 180-degree suicides
        let moveQueue = [];

        function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min)) + min;
        }

        function loop() {
            requestAnimationFrame(loop);

            // Slow down the loop to 15fps (Snake speed)
            if (++count < 6) return;
            count = 0;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Process movement from queue
            if (moveQueue.length > 0) {
                const nextMove = moveQueue.shift();
                if (nextMove === 'left' && snake.dx === 0) { snake.dx = -grid; snake.dy = 0; }
                else if (nextMove === 'up' && snake.dy === 0) { snake.dy = -grid; snake.dx = 0; }
                else if (nextMove === 'right' && snake.dx === 0) { snake.dx = grid; snake.dy = 0; }
                else if (nextMove === 'down' && snake.dy === 0) { snake.dy = grid; snake.dx = 0; }
            }

            snake.x += snake.dx;
            snake.y += snake.dy;

            // DRAW APPLE
            ctx.fillStyle = '#ff0055';
            ctx.shadowBlur = 15; ctx.shadowColor = '#ff0055';
            ctx.fillRect(apple.x, apple.y, grid-1, grid-1);
            ctx.shadowBlur = 0;

            // DRAW SNAKE
            snake.cells.unshift({x: snake.x, y: snake.y});
            if (snake.cells.length > snake.maxCells) snake.cells.pop();

            snake.cells.forEach((cell, index) => {
                ctx.fillStyle = index === 0 ? '#00f2ff' : '#7000ff';
                ctx.fillRect(cell.x, cell.y, grid-1, grid-1);

                // Check Apple Collision
                if (cell.x === apple.x && cell.y === apple.y) {
                    snake.maxCells++;
                    score++;
                    scoreEl.textContent = score;
                    apple.x = getRandomInt(0, 20) * grid;
                    apple.y = getRandomInt(0, 20) * grid;
                }

                // Check Self Collision
                for (let i = index + 1; i < snake.cells.length; i++) {
                    if (cell.x === snake.cells[i].x && cell.y === snake.cells[i].y) resetGame();
                }
            });

            // Check Wall Collision
            if (snake.x < 0 || snake.x >= canvas.width || snake.y < 0 || snake.y >= canvas.height) {
                resetGame();
            }
        }

        async function resetGame() {
            if (score > highscore) {
                highscore = score;
                bestEl.textContent = highscore;
                await fetch('/set_highscore', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({score: highscore})
                });
            }
            alert("COLLISION DETECTED. Score: " + score);
            snake.x = 160; snake.y = 160; snake.cells = []; snake.maxCells = 4;
            snake.dx = grid; snake.dy = 0; score = 0; scoreEl.textContent = 0;
            moveQueue = [];
        }

        document.addEventListener('keydown', (e) => {
            if (e.which === 37) moveQueue.push('left');
            else if (e.which === 38) moveQueue.push('up');
            else if (e.which === 39) moveQueue.push('right');
            else if (e.which === 40) moveQueue.push('down');
        });

        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, highscore=get_highscore())

@app.route('/set_highscore', methods=['POST'])
def set_highscore():
    data = request.get_json()
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)