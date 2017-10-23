import socket
import StringIO
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
board = GameBoard(20,20)

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
def socket_readline(s):
    buff = StringIO.StringIO()
    while True:
        data = s.recv(1)  # Pull what it can
        buff.write(data)
        if '\n' in data: break
    return buff.getvalue().splitlines()[0]

def setup(server,board):
    name = socket_readline(server).strip()
    print "Player name : ",name
    p = Player(name,board)
    print "Created player id"
    msg = str(p.id)+'\n'
    server.send(msg)
    print "Sent player ACK message : ", msg
    return p.id

def thread_callback(sock):
    print "In thread callback"
    player_id = str(setup(sock,board))
    try:
        while True :
            line = socket_readline(sock)     #Format 'id key'
            line = line.strip().split()
            if line[0] == 'Enough':
                board.remove_player(player_id)
                while True:
                    print 'Enough for ',player_id
                sock.close()
                return
            id, key = map(int,line)
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
            sock.send(msg+'\n')
            print 'Grid sent to player ' + str(id)
            #time.sleep(0.01)
    except Exception as e:
        print e
        board.remove_player(player_id)

while True:
    client, addr = server.accept()
    print "Accepted connection ",addr
    start_new_thread(thread_callback, (client,) )
    time.sleep(1)
server.close()