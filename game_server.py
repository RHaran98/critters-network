import socket
import cPickle
from curses import KEY_DOWN,KEY_UP,KEY_LEFT,KEY_RIGHT
import time
from thread import start_new_thread
from critters_game import GameBoard,Player

#Initialize server socket parameters
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 4000)) #All available interfaces, port 4000
server.listen(5) #Accept 5 connections

#Initialize game parameters
board = GameBoard(1,1)

# def setup(f,server,board):
#     while True:
#         try:
#             line = f.readline()
#             line = line.strip()
#             if len(line.split()) > 1:
#                 return
#             else:
#                 p = Player(line,board=board)
#                 id = str(p.id)
#                 server.send('p.id')
#                 break
#         except Exception as e:
#             print 'Error : ', e

def setup(f,server,board):
    p = Player("Name",board)
def thread_callback(sock):
    print "In thread callback"
    f = sock.makefile('r')
    setup(f,server,board)

    while True :
        line = f.readline()     #Format 'id key'
        line = line.strip().split()
        id,key = map(int,line)
        player = board.players[id]

        if key == KEY_RIGHT:
            player.right()
        elif key == KEY_LEFT:
            player.left()
        elif key == KEY_UP:
            player.up()
        elif key == KEY_DOWN:
            player.down()
        board.update()
        print 'Board updated'
        msg = str(board.grid)
        print msg
        server.send(msg)
        print 'Grid sent to client'
        time.sleep(0.01)

while True:
    client, addr = server.accept()
    print "Accepted connection ",addr
    start_new_thread(thread_callback, (client,) )
server.close()