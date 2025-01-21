from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Initialize the game state
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
players = {}  # Store player assignments: {sid: "X" or "O"}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global players
    if len(players) < 2:
        player = "X" if "X" not in players.values() else "O"
        players[request.sid] = player
        emit('assign_player', player)
        emit('update_board', {'board': board, 'current_player': current_player}, broadcast=True)
    else:
        emit('game_full')

@socketio.on('disconnect')
def handle_disconnect():
    global players
    if request.sid in players:
        del players[request.sid]
        reset_game()
        emit('player_disconnected', broadcast=True)

@socketio.on('move')
def handle_move(data):
    global board, current_player
    row = data.get('row')
    col = data.get('col')
    player = players.get(request.sid)

    # Validate if it's the player's turn
    if player != current_player:
        emit('invalid_move', {'message': 'Not your turn!'})
        return

    if board[row][col] == " ":
        board[row][col] = current_player
        winner = check_winner(board)
        tie = is_full(board) and not winner

        if not winner and not tie:
            current_player = "O" if current_player == "X" else "X"

        emit('update_board', {
            'board': board,
            'current_player': current_player,
            'winner': winner,
            'tie': tie
        }, broadcast=True)
    else:
        emit('invalid_move', {'message': 'Cell is already taken!'})

@socketio.on('reset')
def reset_game():
    global board, current_player
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    emit('update_board', {'board': board, 'current_player': current_player}, broadcast=True)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def is_full(board):
    return all(cell != " " for row in board for cell in row)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
