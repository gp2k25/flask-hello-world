from flask import Flask, render_template_string

app = Flask(__name__)

# This template pulls the open-source WASM DOOM engine 
# from a reliable CDN for immediate play.
DOOM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask DOOM</title>
    <style>
        body { background: #000; color: #f00; font-family: 'Courier New', monospace; 
               display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        #dosbox { width: 640px; height: 400px; border: 5px solid #333; box-shadow: 0 0 20px rgba(255,0,0,0.5); }
        .controls { margin-top: 10px; color: #888; font-size: 0.8rem; }
        h1 { margin: 0 0 10px 0; letter-spacing: 5px; }
    </style>
</head>
<body>
    <h1>DOOM</h1>
    <div id="dosbox"></div>
    
    <div class="controls">
        [ARROWS] Move • [CTRL] Fire • [SPACE] Use • [SHIFT] Run • [ALT] Strafe
    </div>

    <script src="https://js-dos.com/v7/build/releases/latest/js-dos.js"></script>
    <script>
        // Initialize the DOS emulator and load DOOM Shareware
        emulators.jsdos(document.getElementById("dosbox"), {
            wdosboxUrl: "https://js-dos.com/v7/build/releases/latest/wdosbox.js",
        }).then((bundle) => {
            bundle.main(["-c", "DOOM.EXE"]);
            // Pointing to a public shareware WAD bundle
            bundle.mountZip("/", "https://js-dos.com/v7/build/bundles/doom.jsdos");
        });
    </script>
</body>
</html>
"""

@app.route('/')
def play_doom():
    return render_template_string(DOOM_HTML)

if __name__ == '__main__':
    # Using threaded=True so the server stays responsive during the WASM load
    app.run(debug=True, port=5000, threaded=True)