import random

class GameBoard:
	'''Maintains co-ordinate data'''
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.grid = [['~']*self.x for _ in range(self.y)]
		self.players = {}
		self.next_id = 0
		self.next_sprite = '`'	#ASCII just before a is '`'

	def add_player(self,player):
		self.next_id += 1
		self.next_sprite = chr(1+ord(self.next_sprite))
		positions = self.get_occupied_positions()
		while True:
			pos = [random.randrange(0,self.x), random.randrange(0,self.y)]
			if pos not in positions:
				break
		self.players[self.next_id] = player
		return self.next_id,self.next_sprite,pos

	def remove_player(self,player_id):
		del self.players[player_id]

	def get_occupied_positions(self):
		return [x.pos for x in self.players.values()]

	def update(self):
		new_grid = [['~']*self.x for _ in range(self.y)]
		for player in self.players.itervalues():
			new_grid[player.pos[0]][player.pos[1]] = player.sprite
		self.grid = new_grid

class Player():
	'''Maintains player data'''
	def __init__(self,name,board):
		self.name = name
		self.id = None
		self.sprite = None
		self.pos = None
		self.board = board
		self.subscribeBoard()

	def subscribeBoard(self):
		self.id,self.sprite,self.pos = self.board.add_player(self)

	def set_pos(self,pos):
		x,y = pos
		if (x < self.board.x and y < self.board.y) and (x >=0 and y >=0):
			if pos not in self.board.get_occupied_positions():
				self.pos = pos

	def right(self):
		x,y = self.pos
		self.set_pos([x+1,y])

	def left(self):
		x,y = self.pos
		self.set_pos([x-1,y])

	def up(self):
		x,y = self.pos
		self.set_pos([x,y-1])

	def down(self):
		x,y = self.pos
		self.set_pos([x,y+1])