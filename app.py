from flask import Flask, render_template_string

app = Flask(__name__)

# We'll use a template string so you don't need a separate HTML file
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Snake</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #2c3e50; color: white; font-family: sans-serif; flex-direction: column; }
        canvas { border: 5px solid #ecf0f1; box-shadow: 0 0 20px rgba(0,0,0,0.5); background: #000; }
        h1 { margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Snake Score: <span id="score">0</span></h1>
    <canvas id="snakeGame" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("snakeGame");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        let box = 20;
        let score = 0;
        let snake = [{x: 9 * box, y: 10 * box}];
        let food = { x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box };
        let d;

        document.addEventListener("keydown", direction);

        function direction(event) {
            if(event.keyCode == 37 && d != "RIGHT") d = "LEFT";
            else if(event.keyCode == 38 && d != "DOWN") d = "UP";
            else if(event.keyCode == 39 && d != "LEFT") d = "RIGHT";
            else if(event.keyCode == 40 && d != "UP") d = "DOWN";
        }

        function draw() {
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i == 0) ? "#2ecc71" : "#27ae60";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
            }

            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(food.x, food.y, box, box);

            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if( d == "LEFT") snakeX -= box;
            if( d == "UP") snakeY -= box;
            if( d == "RIGHT") snakeX += box;
            if( d == "DOWN") snakeY += box;

            if(snakeX == food.x && snakeY == food.y) {
                score++;
                scoreElement.innerHTML = score;
                food = { x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box };
            } else {
                snake.pop();
            }

            let newHead = { x: snakeX, y: snakeY };

            if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || collision(newHead, snake)) {
                clearInterval(game);
                alert("Game Over! Score: " + score);
                location.reload();
            }

            snake.unshift(newHead);
        }

        function collision(head, array) {
            for(let i = 0; i < array.length; i++) {
                if(head.x == array[i].x && head.y == array[i].y) return true;
            }
            return false;
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