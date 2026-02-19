from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Snake Pro</title>
    <style>
        body { 
            display: flex; justify-content: center; align-items: center; 
            height: 100vh; margin: 0; background: #1a1a2e; 
            color: #e94560; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            flex-direction: column; 
        }
        canvas { 
            border: 4px solid #e94560; border-radius: 10px;
            box-shadow: 0 0 30px rgba(233, 69, 96, 0.3); background: #16213e; 
        }
        .stats { margin-bottom: 20px; font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="stats">SCORE: <span id="score">0</span></div>
    <canvas id="snakeGame" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("snakeGame");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        const box = 20;
        let score = 0;
        let snake = [{x: 10 * box, y: 10 * box}];
        let food = { x: Math.floor(Math.random() * 20) * box, y: Math.floor(Math.random() * 20) * box };
        
        let d = "RIGHT"; // Initial direction
        let nextD = "RIGHT"; // Buffer for the next move
        let moveProcessed = true; // Prevents "suicide turns"

        document.addEventListener("keydown", (event) => {
            if (!moveProcessed) return; // Ignore input if we haven't moved yet

            const key = event.keyCode;
            if(key == 37 && d != "RIGHT") { nextD = "LEFT"; moveProcessed = false; }
            else if(key == 38 && d != "DOWN") { nextD = "UP"; moveProcessed = false; }
            else if(key == 39 && d != "LEFT") { nextD = "RIGHT"; moveProcessed = false; }
            else if(key == 40 && d != "UP") { nextD = "DOWN"; moveProcessed = false; }
        });

        function draw() {
            // Update direction from buffer
            d = nextD;
            moveProcessed = true;

            // Clear Canvas
            ctx.fillStyle = "#16213e";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Snake
            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i == 0) ? "#e94560" : "#0f3460";
                ctx.strokeStyle = "#16213e";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }

            // Draw Food
            ctx.fillStyle = "#00d2d3";
            ctx.beginPath();
            ctx.arc(food.x + box/2, food.y + box/2, box/2 - 2, 0, Math.PI * 2);
            ctx.fill();

            // Calculate movement
            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if( d == "LEFT") snakeX -= box;
            if( d == "UP") snakeY -= box;
            if( d == "RIGHT") snakeX += box;
            if( d == "DOWN") snakeY += box;

            let newHead = { x: snakeX, y: snakeY };

            // COLLISION RULES
            // 1. Wall Check
            if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height) {
                gameOver(); return;
            }
            // 2. Self Collision Check
            for(let i = 0; i < snake.length; i++) {
                if(newHead.x == snake[i].x && newHead.y == snake[i].y) {
                    gameOver(); return;
                }
            }

            // 3. Eating Food
            if(snakeX == food.x && snakeY == food.y) {
                score++;
                scoreElement.innerHTML = score;
                food = { x: Math.floor(Math.random() * 20) * box, y: Math.floor(Math.random() * 20) * box };
            } else {
                snake.pop(); // Remove tail
            }

            snake.unshift(newHead); // Add new head
        }

        function gameOver() {
            clearInterval(game);
            alert("GAME OVER! Final Score: " + score);
            location.reload();
        }

        let game = setInterval(draw, 100);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)