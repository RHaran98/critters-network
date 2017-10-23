import StringIO
import socket
import cPickle
import time
from ast import literal_eval
import curses
from curses import KEY_RIGHT

# Initialize socket params
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 4000))
server.settimeout(5)


# f = server.makefile('r')

# Initialize console parameter
stdscr = curses.initscr()
win = curses.newwin(22, 22, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

def socket_readline(s):
    buff = StringIO.StringIO()
    while True:
        data = s.recv(1)  # Pull what it can
        buff.write(data)
        if '\n' in data:
            break
    return buff.getvalue().splitlines()[0]


def get_id(server):
    name = 'generic_name'
    server.send(name + '\n')
    return socket_readline(server).strip()


id = get_id(server)
#print 'Got ID : ', id
key = KEY_RIGHT
stdscr = curses.initscr()
win = curses.newwin(22, 22, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

try:
    while True:
        win.border(0)
        event = win.getch()
        key = event#key if event == -1 else event
        curses.beep()
        if key == 27:
            server.send("Enough\n")
            curses.beep()
            break
        #print 'Sending move'
        data = id + ' ' + str(key) + '\n'
        server.send(data)
        grid = socket_readline(server)
        grid = grid.strip()
        grid = literal_eval(grid)
        # print 'Got grid'
        # print grid
        for x in range(20):
            for y in range(20):
                win.addch(y + 1, x + 1, grid[x][y])  # Offset for border
        win.timeout(150)
        time.sleep(0.01)
except Exception as e:
    server.send('Enough\n')
    server.close()
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
server.close()
