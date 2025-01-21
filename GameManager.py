class Board:
    def __init__(self):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
            print("-" * 9)

    def update(self, row, col, player):
        if self.grid[row][col] == " ":
            self.grid[row][col] = player
            return True
        return False

    def check_winner(self):
        for row in self.grid:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != " ":
                return self.grid[0][col]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
            return self.grid[0][2]
        return None

    def is_full(self):
        return all(cell != " " for row in self.grid for cell in row)

class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.current_player = "X"

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def play_turn(self, row, col):
        if row not in range(3) or col not in range(3):
            return False
        return self.board.update(row, col, self.current_player)

    def run(self):
        print("Welcome to Tic Tac Toe!")
        self.board.display()
        while True:
            print(f"{self.current_player}'s turn.")
            try:
                row = int(input("Enter row (0, 1, 2): "))
                col = int(input("Enter column (0, 1, 2): "))
                if self.play_turn(row, col):
                    self.board.display()
                    winner = self.board.check_winner()
                    if winner:
                        print(f"{winner} wins the game!")
                        break
                    if self.board.is_full():
                        print("The game is a draw!")
                        break
                    self.switch_player()
            except ValueError:
                print("Invalid input. Please enter numbers only.")
