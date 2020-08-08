from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yeet'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['FLASK_ENV'] = 'development'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
board = boggle_game.make_board()
high_score = 0
games_played = 0

@app.route('/')
def game():
    """Displays the home page"""
    global board
    global high_score
    global games_played
    session['board'] = board
    if session.get('high-score'):
        high_score = session['high-score']
    if session.get('games-played'):
        games_played = session['games-played']
    return render_template('game.html', board=board, size=len(board), high_score=high_score, games_played=games_played)

@app.route('/guess')
def guess():
    """Takes a request from the front end and checks if the given word is valid"""
    word = request.args['word']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/game-over')
def game_over():
    """Takes a request from the front end at the end of a game to check if a new high score has been set"""
    global games_played
    global high_score
    if session.get('games-played'):
        games_played = session['games-played']
    games_played += 1
    session['games-played'] = games_played
    score = int(request.args['score'])
    if session.get('high-score'):
        high_score = session['high-score']
    new_high_score = check_high_score(score, high_score)
    if new_high_score:
        high_score = new_high_score
        session['high-score'] = high_score
        new_high_score = True
    return jsonify({'new_high_score': new_high_score, 'games_played': games_played})

@app.route('/new-game')
def reset_game():
    """Creates a new board and redirects to the home page"""
    global board
    board = boggle_game.make_board()
    return redirect('/')

def check_high_score(score, high_score):
    """Checks if a new high score has been set
    If a new high score has been set, returns the new high score
    If not, returns False"""
    if score > high_score:
        return score
    else:
        return False