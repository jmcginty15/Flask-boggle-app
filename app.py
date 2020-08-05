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

@app.route('/')
def homepage():
    session['board'] = board
    return render_template('game.html', board=board, size=len(board))

@app.route('/guess', methods=['POST'])
def guess():
    word = request.args['word']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})