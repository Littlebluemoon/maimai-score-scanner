from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from app import routes

from services.ScoreScanner import ScoreScanner

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(routes.bp)

score_scanner = ScoreScanner(socketio)

score_scanner.start()

# @socketio.on("score_scanner")
# def handle_ss():
#     score_scanner.subscribe()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000,allow_unsafe_werkzeug=True)