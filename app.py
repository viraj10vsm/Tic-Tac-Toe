from flask import Flask, render_template, redirect, url_for, request
from GameManager import TicTacToe

app = Flask(__name__)

# Initialize the game
game = TicTacToe()

@app.route('/')
def login():
    """Login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    """Handle login logic (template only)."""
    username = request.form['username']
    password = request.form['password']

    # Simulate login check (no session or database handling)
    return redirect(url_for('game_view'))

@app.route('/register')
def register():
    """Registration page."""
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def handle_register():
    """Handle registration logic (template only)."""
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Simulate registration logic
    return "<h1>Registration Successful</h1><p>Click <a href='/'>here</a> to login.</p>"

@app.route('/game')
def game_view():
    """Game screen route."""
    # Render the game template with the current board and player
    board = game.board.grid
    current_player = game.current_player
    winner = game.board.check_winner()
    draw = game.board.is_full() and winner is None

    return render_template('gamescreen.html', board=board, current_player=current_player, winner=winner, draw=draw)

@app.route('/move/<int:row>/<int:col>')
def make_move(row, col):
    """Handle a move in the game."""
    # Check if the game has already ended
    winner = game.board.check_winner()
    draw = game.board.is_full()
    if winner or draw:
        return redirect(url_for('game_view'))

    # Process the move if the game is still ongoing
    if game.play_turn(row, col):
        winner = game.board.check_winner()
        if winner or game.board.is_full():
            return redirect(url_for('game_view'))
        game.switch_player()
    return redirect(url_for('game_view'))

@app.route('/reset')
def reset_game():
    """Reset the game state."""
    global game
    game = TicTacToe()
    return redirect(url_for('game_view'))

if __name__ == '__main__':
    app.run(debug=True)
