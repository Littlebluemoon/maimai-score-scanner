from flask import Blueprint, render_template

import services.ScoreScanner

bp = Blueprint('main', __name__)

@bp.route('/')
def hello_world():
    return 'Hello, World!'

@bp.route('/current-score')
def current_score():
    return render_template('index.html')