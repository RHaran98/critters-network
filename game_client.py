import socket
import cPickle
import time
from ast import literal_eval
import curses
from curses import KEY_RIGHT
#Initialize socket params
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 4000))
server.settimeout(1000000)
f = server.makefile('r')

#Initialize console parameter

# stdscr = curses.initscr()
# win = curses.newwin(22, 22, 0, 0)
# win.keypad(1)
# curses.noecho()
# curses.curs_set(0)
# win.border(0)
# win.nodelay(1)

def get_id(f,server):
    name = 'generic_name'#raw_input('Enter player name : ')
    server.send(name+'\n')
    return int(f.readline().strip())

id = '1'#get_id(f,server)
#print 'Got ID : ',id
key = KEY_RIGHT
# stdscr = curses.initscr()
# win = curses.newwin(22, 22, 0, 0)
# win.keypad(1)
# curses.noecho()
# curses.curs_set(0)
# win.border(0)
# win.nodelay(1)

while True:
    # win.border(0)
    # event = win.getch()
    # key = key if event == -1 else event
    # if key == 27:
    #     break
    print 'Sending move'
    data = id+' '+ str(key) +'\n'
    server.send(data)
    print 'Sent'
    print 'Receving grid'
    grid = f.readline()
    grid = grid.strip()
    grid = literal_eval(grid)
    print 'Got grid'
    print grid
    # for x in range(20):
    #     for y in range(20):
    #         win.addch(y + 1, x + 1, grid[x][y])  # Offset for border
    # win.timeout(150)
    time.sleep(0.1)

# curses.nocbreak()
# stdscr.keypad(0)
# curses.echo()
# curses.endwin()
# server.close()
