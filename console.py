import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from critters_game import GameBoard,Player
stdscr = curses.initscr()
def main():
    win = curses.newwin(22, 22, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    board = GameBoard(20,20)
    p1 = Player("Player-1", board)
    key = KEY_RIGHT
    while True:
        win.border(0)
        event = win.getch()

        key = key if event == -1 else event
        if key == 27:
            break
        if key == KEY_RIGHT:
            p1.right()
        elif key == KEY_LEFT:
            p1.left()
        elif key == KEY_UP:
            p1.up()
        elif key == KEY_DOWN:
            p1.down()
        board.update()
        key = -1
        for x in range(board.x):
            for y in range(board.y):
                win.addch(y+1,x+1,board.grid[x][y]) # Offset for border
        win.timeout(150)
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    try :
        main()
    except Exception as e:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        print 'Error : ', e