import turtle
import random

# Setting up the main screen
screen = turtle.Screen()
screen.title("Tic Tac Toe")
screen.setup(width=600, height=600)
screen.bgcolor("lightgreen")

# Global variables
player1 = "X"
bot = "O"
current_player = player1
game_state = [""] * 9
game_over = False
bot_level = "Easy"

# Drawing the board
board = turtle.Turtle()
board.hideturtle()
board.speed(0)
board.pensize(5)

def draw_board():
    board.penup()
    board.goto(-300, 100)
    board.pendown()
    board.forward(600)
    board.penup()
    board.goto(-300, -100)
    board.pendown()
    board.forward(600)
    board.penup()
    board.goto(-100, 300)
    board.right(90)
    board.pendown()
    board.forward(600)
    board.penup()
    board.goto(100, 300)
    board.pendown()
    board.forward(600)

# Drawing X and O
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.pensize(3)

def draw_x(x, y):
    drawer.penup()
    drawer.goto(x - 60, y + 60)
    drawer.pendown()
    drawer.goto(x + 60, y - 60)
    drawer.penup()
    drawer.goto(x + 60, y + 60)
    drawer.pendown()
    drawer.goto(x - 60, y - 60)
    drawer.penup()

def draw_o(x, y):
    drawer.penup()
    drawer.goto(x, y - 60)
    drawer.pendown()
    drawer.circle(60)
    drawer.penup()

def display_message(message):
    board.clear()
    draw_board()
    board.penup()
    board.goto(0, -250)
    board.color("black")
    board.write(message, align="center", font=("Arial", 24, "normal"))

def click_handler(x, y):
    global current_player, game_over
    
    if game_over:
        return
    
    if current_player == player1:
        row = int((y + 300) // 200)
        col = int((x + 300) // 200)
        cell = row * 3 + col

        if game_state[cell] == "":
            make_move(cell)
            if not game_over:
                bot_move()

def make_move(cell):
    global current_player, game_over
    
    game_state[cell] = current_player
    row = cell // 3
    col = cell % 3
    cell_center_x = col * 200 - 200 + 100 - 100
    cell_center_y = -(300 - row * 200 - 100)
    if current_player == player1:
        draw_x(cell_center_x, cell_center_y)
    else:
        draw_o(cell_center_x, cell_center_y)
    if check_winner():
        display_message(f"Player {current_player} wins!")
        game_over = True
        return
    if all(cell != "" for cell in game_state):
        display_message("It's a tie!")
        game_over = True
        return
    current_player = bot if current_player == player1 else player1

def bot_move():
    if bot_level == "Easy":
        easy_bot_move()
    elif bot_level == "Medium":
        medium_bot_move()
    elif bot_level == "Hard":
        hard_bot_move()

def easy_bot_move():
    available_cells = [i for i, cell in enumerate(game_state) if cell == ""]
    if available_cells:
        cell = random.choice(available_cells)
        make_move(cell)

def medium_bot_move():
    for player in [bot, player1]:  # First check if bot can win, then block player1
        for i in range(9):
            if game_state[i] == "":
                game_state[i] = player
                if check_winner():
                    game_state[i] = bot
                    make_move(i)
                    return
                game_state[i] = ""
    easy_bot_move()

def hard_bot_move():
    # Check for winning or blocking moves
    for player in [bot, player1]:  # First check if bot can win, then block player1
        for i in range(9):
            if game_state[i] == "":
                game_state[i] = player
                if check_winner():
                    game_state[i] = bot
                    make_move(i)
                    return
                game_state[i] = ""
    # If no winning or blocking move found, choose the center if available
    if game_state[4] == "":
        make_move(4)
        return
    # If no center move, choose a random available cell
    easy_bot_move()

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    
    for combo in winning_combinations:
        if game_state[combo[0]] == game_state[combo[1]] == game_state[combo[2]] != "":
            return True
    return False

def choose_difficulty():
    global bot_level
    difficulty = turtle.textinput("Choose Bot Difficulty", "Choose difficulty: Easy, Medium, Hard, Random").capitalize()
    if difficulty == "Random":
        bot_level = random.choice(["Easy", "Medium", "Hard"])
    else:
        bot_level = difficulty

def start_game():
    choose_difficulty()
    global current_player, game_state, game_over
    current_player = player1
    game_state = [""] * 9
    game_over = False
    display_message(f"You chose {bot_level} difficulty level.")
    draw_board()
    screen.onclick(click_handler)
    screen.listen()

start_game()

while True:
    screen.update()
turtle.mainloop()
