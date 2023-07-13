"""
The program implements the game of Connect Four for two players.
* Modules usage
    * turtle
* User interface
    * A welcome page
    * A chessboard and mouse trackers.
    * Colored tokens for the dropped tokens.
      Default color: Red for player 1, Blue for player 2.
    * Lighter-colored tokens when the mouse is on the column.
      (Advanced highlighting only)
    * Colored trackers bar when the mouse is on the column.
    * A title bar that shows the current/winning player.
    * A message box that shows the result of the game
      Font: Comic Sans MS, 20, bold.
* Game information
    * The size of the chessboard is 8x8.
    * The size of the token is 60x60 (pixels), or radius 30.
    * The size of the mouse tracker is 60x10 (pixels).
    * The size of the window is 640x680 (pixels).
* Program structure
    * Basic element drawing functions
        * draw_token
        * draw_rectangle
        * highlight_token
    * Game setting up and ending functions
        * init
        * setup_welcome
        * setup_chessboard
        * setup_highlight
        * ending
    * Game organizing functions
        * checkmate
        * drop_token
        * track_position
        * get_position
    * Main part
* Assignment information
    * Course: CSC 1002
    * Assignment No. 2
    * Author: frankchenfu
    * Date: Mar 17, 2023
    * Language: Python 3.6.8 (64-bit)
    * Standard: PEP 8
"""

import turtle

"""
Definitions for global variables.
@param g_chessboard
    A two dimensional list that stores the chessboard,
    where False represents player 1 and True represents player 2.
@param g_turtle
    The turtle object used to draw the chessboard.
@param g_screen
    The screen object used to draw the chessboard.
@param g_canvas
    The canvas of the screen, allowing mouse tracking.
@param g_col
    The column of the chessboard that the mouse is currently on.
@param g_player
    The player that is currently playing.
    False represents player 1 and True represents player 2.
@param g_highlight
    A boolean value representing whether advanced highlighting is enabled.
@param g_colors
    A dictionary that stores the colors used in the game:
    * "1p" for player 1's token,
    * "2p" for player 2's token,
    * "1p_a" for player 1's attempt when the mouse is on the column,
    * "2p_a" for player 2's attempt when the mouse is on the column,
    * "win" for the winning tokens,
    * "bar" for the column tracker bar,
    * "bg" for the background.
"""
g_chessboard = [[] for i in range(8)]
g_turtle = turtle.Turtle()
g_screen = turtle.Screen()
g_canvas = g_screen.getcanvas()
g_col = 0
g_player = False
g_highlight = False
g_colors = {
    "1p": "#FF0000", "2p": "#0000FF",
    "1p_a": "#FFE9E9", "2p_a": "#E9E9FF",
    "win": "#C0F011",
    "bar": "#000000", "bg": "#FFFFFF"
}

# The following three functions are used to draw or highlight the basic
# elements of the chessboard.
"""
Draws the column tracker bar.
* The size of the tracker bar is expected to be 60x10 in pixels actually.
* Since the pen's width is 5 pixels, the length has to be 5 pixels longer
  in order to keep the bar's size unchanged.
* The status "penup" is expected before and after the function call.
@return
    None.
"""
def draw_rectangle() -> None:
    g_turtle.pendown()
    g_turtle.begin_fill()
    g_turtle.forward(65)
    g_turtle.right(90)
    g_turtle.forward(15)
    g_turtle.right(90)
    g_turtle.forward(65)
    g_turtle.right(90)
    g_turtle.forward(15)
    g_turtle.right(90)
    g_turtle.end_fill()
    g_turtle.penup()

"""
Draws a token at the given position.
* The status "penup" is expected before and after the function call.
* The size of the token is expected to be 60x60 in pixels actually.
  Since the pen's width is 5 pixels, the radius has to be 2.5 pixels larger,
  giving the radius approximately 33 pixels in total.
@param x
    The column of the token.
@param y
    The row of the token.
@param color
    The color of the token.
    The color should be one of the following:
    * "1p" for player 1's token,
    * "2p" for player 2's token,
    * "1p_a" for player 1's token when the mouse is on the column,
    * "2p_a" for player 2's token when the mouse is on the column.
@return
    None.
"""
def draw_token(x: int, y: int, color: str) -> None:
    g_turtle.goto(x * 80 + 40, y * 80)
    g_turtle.pendown()
    g_turtle.color(g_colors["bg"], g_colors[color])
    g_turtle.begin_fill()
    g_turtle.circle(33)
    g_turtle.end_fill()
    g_turtle.penup()

"""
Highlights the token at the given position.
* Draws a circle around the winning token with the color "win".
* The status "penup" is expected before and after the function call.
* Should be call if and only if it's a winning token.
@param x
    The column of the token.
@param y
    The row of the token.
@return
    None.
"""
def highlight_token(x: int, y: int) -> None:
    g_turtle.goto(x * 80 + 40, y * 80)
    g_turtle.pendown()
    g_turtle.color(g_colors["win"])
    g_turtle.circle(33)
    g_turtle.penup()


# The following five functions are used to set up or end the game.
"""
Initializes the tools used to draw the chessboard.
* The status "penup" is expected after the function call.
* Should be called once before any other functions.
@param setscreen
    Whether to set up the "screen" object.
    Should be set to True if the function is called for the first time.
@return
    None.
"""
def init(setscreen: bool) -> None:
    if setscreen:
        g_screen.setup(640, 720)  # Set the size of the screen
        g_screen.setworldcoordinates(10, -70, 630, 630)
        g_screen._root.resizable(False, False)  # Disable resizing
        g_screen.tracer(0)  # Disable animation
        g_screen.title("Connect Four")  # Set the title
    g_turtle.speed("fastest")
    g_turtle.hideturtle()  # Hide the turtle
    g_turtle.width(5)  # Set the width of the pen
    g_turtle.penup()  # Set the pen to "penup" status

"""
Sets up the welcome page, introducing the tokens for the players.
* The status "penup" is expected before the function call.
* First prints the welcome message, then draws the tokens for the players.
* Allows the players to start the game by pressing <Enter>.
@return
    None.
"""
def setup_welcome() -> None:
    g_turtle.goto(320, 540)
    g_turtle.write("Welcome to Connect Four!", align="center",
                   font=("Comic Sans MS", 20, "bold"))
    draw_token(2, 5, "1p")  # Draw the token for player 1
    g_turtle.goto(280, 420)
    g_turtle.color(g_colors["bar"])
    g_turtle.write("-    Player 1", align="left",
                   font=("Comic Sans MS", 20, "bold"))
    draw_token(2, 4, "2p")  # Draw the token for player 2
    g_turtle.goto(280, 340)
    g_turtle.color(g_colors["bar"])
    g_turtle.write("-    Player 2", align="left",
                   font=("Comic Sans MS", 20, "bold"))
    g_turtle.goto(320, 180)
    g_turtle.write("Press <Enter> to start normal game!", align="center",
                   font=("Comic Sans MS", 16, "bold"))
    g_turtle.goto(320, 140)
    g_turtle.write("Or press <Space> to start with advanced highlight.",
                   align="center", font=("Comic Sans MS", 16, "bold"))
    g_screen.update()
    g_screen.onkeypress(setup_highlight, " ")
    g_screen.onkeypress(setup_chessboard, "Return")

"""
Sets up for the game with advanced highlight.
@return
    None.
"""
def setup_highlight() -> None:
    global g_highlight
    g_highlight = True
    setup_chessboard()

"""
Sets up the initial chessboard and mouse tracking.
* The status "penup" is expected before the function call.
* First sets up the mouse tracking, then draws the chessboard.
* Allows the players to play the game until the game ends.
@return
    None.
"""
def setup_chessboard() -> None:
    g_screen.reset()  # Clear the welcome page
    init(setscreen=False)  # Set up the tools
    g_screen.onkeypress(None, "Return")  # Withdraw the bond for <Enter>
    g_screen.onkeypress(None, " ")  # Withdraw the bond for <Space>
    g_screen.title("Connect Four - Player 1's turn")  # Set the current player
    g_screen.onclick(get_position)  # Listen for mouse clicks
    g_canvas.bind("<Motion>", track_position)  # Set up mouse tracking

    # drawing the tracking bars.
    g_turtle.color(g_colors["bg"], g_colors["bar"])
    g_turtle.goto(8, -10)
    for i in range(8):
        draw_rectangle()
        g_turtle.forward(80)
    g_screen.update()

"""
Give ending information and exit the game.
* The status "penup" is expected before and after the function call.
* Highlights the winning tokens if there is a winning player.
* Prints the ending information (title and screen).
* Allows the players to exit the game by pressing <Enter>.
@param checkmate_result
    * A list with four tuples, each tuple representing a winning token,
    * Or an empty list if the game is tied.
@return
    None.
"""
def ending(checkmate_result: list) -> None:
    for i, j in checkmate_result:  # Highlight the winning tokens
        highlight_token(i, j)
    g_screen.onclick(None)  # Stop listening for mouse clicks
    g_canvas.unbind("<Motion>")  # Stop tracking the mouse
    if checkmate_result:
        checkmate_info = "Winner! Player %d!" % (2 if g_player else 1)
    else:
        checkmate_info = "Game Tied!"
    g_screen.title("Connect Four - " + checkmate_info)
    g_turtle.goto(320, -65)
    g_turtle.color("black")
    g_turtle.write(checkmate_info + " Press <Enter> to exit.", align="center",
                   font=("Comic Sans MS", 20, "bold"))
    g_screen.update()
    g_screen.onkeypress(g_screen.bye, "Return")  # Allow the players to exit.


# The following four functions are used to play the game.
"""
Checks whether the game is over.
* Checks the four directions for a winning token:
    * horizontal,
    * vertical,
    * diagonal (top-left to bottom-right),
    * diagonal (top-right to bottom-left).
* Checks whether the game is tied.
    * The game is tied if the chessboard is full and no one wins.
@return
    * A list with four tuples, each tuple representing a winning token
      if there is a winning player.
    * An empty list if the game is tied.
    * None if the game is not over.
"""
def checkmate() -> list:
    # Check the horizontal direction
    for i in range(8):
        height = len(g_chessboard[i])
        if height < 4:
            continue
        if len(set(g_chessboard[i][-4:])) == 1:
            return [(i, j) for j in range(height - 4, height)]

    # Check the vertical direction
    for i in range(5):
        height = [len(g_chessboard[k]) for k in range(i, i + 4)]
        for j in range(min(height)):
            if len(set([g_chessboard[k][j] for k in range(i, i + 4)])) == 1:
                return [(k, j) for k in range(i, i + 4)]

    # Check the diagonal direction(top-right to bottom-left)
    for i in range(5):
        height = [len(g_chessboard[k]) - k + i for k in range(i, i + 4)]
        for j in range(min(height)):
            if len(set([g_chessboard[k][j - i + k]
                   for k in range(i, i + 4)])) == 1:
                return [(k, j - i + k) for k in range(i, i + 4)]

    # Check the diagonal direction(top-left to bottom-right)
    for i in range(3, 8):
        height = [len(g_chessboard[k]) - i + k for k in range(i - 3, i + 1)]
        for j in range(min(height)):
            if len(set([g_chessboard[k][j + i - k]
                   for k in range(i - 3, i + 1)])) == 1:
                return [(k, j + i - k) for k in range(i - 3, i + 1)]

    # if there is no winning player, then a full chessboard means a tie.
    for i in range(8):
        if len(g_chessboard[i]) != 8:
            break
    else:  # The game is tied
        return []

    # The game is not over.
    return None

"""
Drops a token into the chessboard.
* Maintains both the frontend (screen) and backend (list) of the game.
* The status "penup" is expected before and after the function call.
@param player
    * False if the current player is player 1.
    * True if the current player is player 2.
@return
    * True if the token is successfully dropped.
    * False if the token cannot be dropped.
"""
def drop_token(player) -> bool:
    col = g_col
    if len(g_chessboard[col]) == 8:  # The column is full
        return False
    g_chessboard[col].append(player)
    draw_token(col, len(g_chessboard[col]) - 1, "2p" if player else "1p")
    g_screen.update()
    return True

"""
Tracks the mouse position and draws the tracking bars and attempting tokens.
* The status "penup" is expected before and after the function call.
@param event
    * The mouse event caught by the canvas if event is not None,
      then modify the tracking bars and attempting tokens.
    * Just update the tracking bars and attempting tokens if event is None.
@return
    None.
"""
def track_position(event=None) -> None:
    global g_col
    if event is not None:  # Modify the tracking bars and attempting tokens
        new_col = int(event.x // 80)
        if new_col < 0 or new_col > 7:
            return
        if new_col != g_col:  # Modify if the mouse is moved to a new column
            g_turtle.goto(g_col * 80 + 8, -10)
            g_turtle.color(g_colors["bg"], g_colors["bar"])
            draw_rectangle()
            if g_highlight and len(g_chessboard[g_col]) < 8:
                draw_token(g_col, len(g_chessboard[g_col]), "bg")
            g_col = new_col
            g_turtle.goto(g_col * 80 + 8, -10)
            g_turtle.color(
                g_colors["2p" if g_player else "1p"], g_colors["bar"])
            draw_rectangle()
            if g_highlight and len(g_chessboard[g_col]) < 8:
                draw_token(g_col, len(g_chessboard[g_col]),
                           "2p_a" if g_player else "1p_a")
    else:  # Update the tracking bars and attempting tokens
        g_turtle.goto(g_col * 80 + 8, -10)
        g_turtle.color(g_colors["2p" if g_player else "1p"], g_colors["bar"])
        draw_rectangle()
        if g_highlight and len(g_chessboard[g_col]) < 8:
            draw_token(g_col, len(g_chessboard[g_col]),
                       "2p_a" if g_player else "1p_a")
    g_screen.update()

"""
Gets the position of the mouse click and drops a token.
* The status "penup" is expected before and after the function call.
* Checks whether the game is over after the token is dropped.
* Changes the player if the game is not over.
* Does nothing if the token cannot be dropped.
@param x
    The x coordinate of the mouse click.
@param y
    The y coordinate of the mouse click.
@return
    None.
"""
def get_position(x: int, y: int) -> None:
    global g_col
    global g_player
    g_col = int((x + 2) // 80)  # Get the column of the mouse click
    if g_col < 0 or g_col > 7:  # The mouse click is out of the chessboard
        return
    if not drop_token(g_player):  # The token cannot be dropped
        return
    checkmate_result = checkmate()
    if checkmate_result is not None:  # The game is over
        ending(checkmate_result)
        return
    g_player = not g_player
    g_screen.title("Connect Four - Player %d's turn" % (2 if g_player else 1))
    track_position()  # Update the tracking bars and attempting tokens


if __name__ == "__main__":  # The main function
    init(setscreen=True)  # Initialize the game
    setup_welcome()  # Setup the welcome screen and start the game
    g_screen.listen()  # Listen to the mouse events
    g_screen.mainloop()  # Start the mainloop