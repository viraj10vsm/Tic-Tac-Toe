from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response, session
from GameManager import TicTacToe
from models import db, User, GameHistory
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

''' APP CONFIGURATIONS '''
app.config['SECRET_KEY'] = '70582bdc537545f19bf99bacdf2fc5da'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize SQLAlchemy with Flask app
game = TicTacToe()  # Initialize the game


''' JWT Token Decorator '''
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')  # Retrieve token from cookies
        if not token:
            return redirect(url_for('login'))
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated


''' Routes '''
@app.route('/')
def login():
    if 'logged_in' not in session:
        return render_template('login.html')  # Render the login page
    return redirect(url_for('game_view'))


@app.route('/login', methods=['POST'])
def handle_login():
    """Handle user login with JWT."""
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['logged_in'] = True
        session['username'] = username  # Store the username in session
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        response = make_response(redirect(url_for('game_view')))
        response.set_cookie('token', token)  # Set JWT token in cookies
        return response

    return make_response('Invalid credentials', 401)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return 'Username already exists.', 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "<h1>Registration Successful</h1><p>Click <a href='/'>here</a> to login.</p>"

    return render_template('register.html')


@app.route('/logout', methods=['POST'])
def logout():
    """Logout the user."""
    session.pop('logged_in', None)
    session.pop('username', None)  # Remove username from session
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')  # Remove JWT token
    return response


@app.route('/game')
@token_required
def game_view():
    """Game screen route."""
    board = game.board.grid
    current_player = game.current_player
    winner = game.board.check_winner()
    draw = game.board.is_full() and winner is None

    return render_template('gamescreen.html', board=board, current_player=current_player, winner=winner, draw=draw)


@app.route('/move/<int:row>/<int:col>')
@token_required
def make_move(row, col):
    """Handle a move in the game."""
    winner = game.board.check_winner()
    draw = game.board.is_full()
    if winner or draw:
        return redirect(url_for('game_view'))

    if game.play_turn(row, col):
        winner = game.board.check_winner()
        if winner or game.board.is_full():
            save_game_history(winner)
            return redirect(url_for('game_view'))
        game.switch_player()
    return redirect(url_for('game_view'))


@app.route('/reset')
@token_required
def reset_game():
    """Reset the game state."""
    global game
    game = TicTacToe()
    return redirect(url_for('game_view'))


@app.route('/view_history')
@token_required
def view_history():
    """View the match history."""
    history = GameHistory.query.order_by(GameHistory.timestamp.desc()).all()
    return render_template('view_history.html', history=history)


''' Helper to Save Game History '''
def save_game_history(winner):
    """Save game result to the database."""
    new_history = GameHistory(
        winner=winner if winner else "Draw",
        timestamp=datetime.utcnow()
    )
    db.session.add(new_history)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in the database
    app.run(debug=True)
