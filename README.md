# Tic Tac Toe  Game

This project implements a multiplayer Tic Tac Toe game using **Flask**, **Flask-SocketIO**, and **SQLite**. Players can register, log in, play against each other in real time, and view their game history.

---

## Features

1. **User Authentication**
   - Register and log in with email and password.
   - Passwords are securely stored (hashed).

2. **Multiplayer Game**
   - Real-time game using Python SocketIO.
   - Players can play as X or O and take turns.
   - Game ends with a winner, draw, or quit condition.

3. **Game History**
   - Stores match details in an SQLite database.
   - Includes players' names, results, and timestamps.
   - Users can view their match history and overall statistics.

---

## Setup Instructions

```bash

### 1. Clone the Repository
git clone https://github.com/your-repo/tic-tac-toe-multiplayer.git
cd tic-tac-toe-multiplayer

2. Install Dependencies
Create a virtual environment and install the required packages:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Initialize the Database
Run the following script to create the SQLite database and tables:
python init_db.py

4. Run the Application
Start the Flask app with Flask-SocketIO:

python app.py
The application will be accessible at http://127.0.0.1:5000.


# Project Structure

tic-tac-toe/
│
├── templates/               # HTML files (login, register, game screen, results page)
├── static/                  # CSS and JS files
├── app.py                   # Main Flask application
├── GameManager.py           # Game logic and board handling
├── init_db.py               # Script to initialize the database
├── requirements.txt         # Required Python packages
└── README.md                # Project documentation

Technologies Used
Frontend: HTML, CSS, Jinja Templates
Backend: Flask, Flask-SocketIO
Database: SQLite
WebSocket Communication: Python SocketIO
Future Improvements
Add a leaderboard to display top players.
Include real-time chat functionality.
Enhance the UI with animations and improved responsiveness.
Author
Created by Viraj Mahale. Feel free to contribute to this project by creating a pull request or reporting issues.

---

### **Key Files for Implementation**

1. **`app.py`**
   - Flask app for user login, registration, game room, and history retrieval.
   - Integrates SocketIO for real-time gameplay.

2. **`GameManager.py`**
   - Handles the game logic and validation.

3. **`init_db.py`**
   - Initializes the SQLite database with required tables.

---
