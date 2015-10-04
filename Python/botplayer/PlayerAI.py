from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *
from random import randint

class PlayerAI:
	def __init__(self):
		#maps the direction to integer values
		self.intDir = {Direction.UP:0, 
				Direction.DOWN:1,
				Direction.LEFT:2,
				Direction.RIGHT:3}

		#maps the direction to rotations
		self.comDir = {Direction.UP:Move.FACE_UP, 
				Direction.DOWN:Move.FACE_DOWN,
				Direction.LEFT:Move.FACE_LEFT,
				Direction.RIGHT:Move.FACE_RIGHT}

		#maps integer values to directions
		self.intComDir = {	0:Move.FACE_UP, 
							1:Move.FACE_DOWN,
							2:Move.FACE_LEFT,
							3:Move.FACE_RIGHT,
							4:Move.FORWARD,
							5:Move.FORWARD,
							6:Move.FORWARD,
							7:Move.FORWARD,
							8:Move.SHOOT,
							9:Move.SHOOT,
							10:Move.SHOOT,
							11:Move.SHOOT}
		self.checkOffsets = [(0,2), (0,1), (0,-1), (0,-2),
						(-2,0),(-1,0),(1,0), (2, 0)]
		self.init = False
		self.turret_cells = []
		self.lastTurn = -1
		pass

	def get_move(self, gameboard, player, opponent):
		if self.init == False:
			self.init1(gameboard, player)

		result = self.colDet(gameboard, player)
		if result != -1 and result != Move.NONE:
			return result

		x = player.x
		y = player.y

		if {x, y} in self.turret_cells:
			return Move.FORWARD

		while 1:
			intMove = randint(0,11)
			move = self.intComDir[intMove]
			if move == Move.FORWARD:
				if player.direction == Direction.UP:
					temp = self.calcPos(x, y-1)
				elif player.direction == Direction.DOWN:
					temp = self.calcPos(x, y+1)
				elif player.direction == Direction.LEFT:
					temp = self.calcPos(x-1, y)
				else:
					temp = self.calcPos(x+1, y)
				temp2 = {temp[0], temp[1]}
				if self.bulletsAround(gameboard, player.direction, temp[0], temp[1]):
					continue
				elif temp2 in self.turret_cells:
					continue
				elif gameboard.is_wall_at_tile(temp[0], temp[1]):
					continue
				else:
					self.lastTurn = intMove
					return move 	#break
			elif intMove < 4:
				if self.lastTurn < 4:
					continue
				else:
					self.lastTurn = intMove
					break
			else:
				self.lastTurn = intMove
				break

		#print ("rand", move)
		return move

	def load_turrets(self, gameboard):
		for turret in gameboard.turrets:
			self.turret_cells.append({turret.x, turret.y})
			for x in range (1, 5):
				if turret.x + x > gameboard.width - 1:
					target_cell = 0 + x
				else:
					target_cell = turret.x + x
				temp = self.calcPos(target_cell, turret.y)
				if gameboard.is_wall_at_tile(temp[0],temp[1]):
					break
				else:
					self.turret_cells.append({target_cell, turret.y})
			for x in range (1, 5):
				if turret.x - x < 0:
					target_cell = gameboard.width - x - 1
				else:
					target_cell = turret.x - x				
				temp = self.calcPos(target_cell, turret.y)
				if gameboard.is_wall_at_tile(temp[0],temp[1]):
					break
				else:
					self.turret_cells.append({target_cell, turret.y})
			for x in range (1, 5):
				if turret.y + x > gameboard.height - 1:
					target_cell = 0 + x
				else:
					target_cell = turret.y + x

				temp = self.calcPos(turret.x, target_cell)
				if gameboard.is_wall_at_tile(temp[0],temp[1]):
					break
				else:
					self.turret_cells.append({turret.x, target_cell})
			for x in range (1, 5):
				if turret.y - x < 0:
					target_cell = gameboard.height - x -1
				else:
					target_cell = turret.y - x
				temp = self.calcPos(turret.x, target_cell)
				if gameboard.is_wall_at_tile(temp[0],temp[1]):
					break
				else:
					self.turret_cells.append({turret.x, target_cell})

	def opponentDirX(self, player, opponent):
		if player.x == opponent.x:
			return -1
		elif player.x - opponent.x < 0:
			return self.intDir[Direction.RIGHT]
		else:
			return self.intDir[Direction.LEFT]

	def init1(self, gameboard, player):
		#max length in terms of gameboard; zero indexed
		self.maxX = gameboard.width
		self.maxY = gameboard.height
		self.init = True
		self.stuck = False
		self.load_turrets(gameboard)


	def calcPos(self, x, y):
		if x < 0:
			x = self.maxX + x
		elif x >= self.maxX:
			x = x - self.maxX
		if y < 0:
			y = self.maxY + y
		elif y >= self.maxY:
			y = y - self.maxY
		return (x, y)


	def colDet(self, gameboard, player):
		x = player.x
		y = player.y

		pos = self.calcPos(x, y+1)
		if gameboard.are_bullets_at_tile(pos[0], pos[1]):
			for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:
				if b.direction == Direction.UP:
					if player.direction != Direction.DOWN:
						if player.direction == b.direction:
							self.stuck = True
						return Move.FORWARD
					else:
						return -1
		pos = self.calcPos(x, y-1)
		if gameboard.are_bullets_at_tile(pos[0], pos[1]):
			for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:
				if b.direction == Direction.DOWN:
					if player.direction != Direction.UP:
						if player.direction == b.direction:
							self.stuck = True
						return Move.FORWARD
					else:
						return -1
		pos = self.calcPos(x+1, y)
		if gameboard.are_bullets_at_tile(pos[0], pos[1]):
			for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:
				if b.direction == Direction.LEFT:
					if player.direction != Direction.RIGHT:
						if player.direction == b.direction:
							self.stuck = True
						return Move.FORWARD
					else:
						return -1
		pos = self.calcPos(x-1, y)
		if gameboard.are_bullets_at_tile(pos[0], pos[1]):
			for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:
				if b.direction == Direction.RIGHT:
					if player.direction != Direction.LEFT:
						if player.direction == b.direction:
							self.stuck = True
						return Move.FORWARD
					else:
						return -1
		
		#---------------------------------------------------------------------------
		tempPos = [(x, y+2), (x, y-2), (x+2, y), (x-2, y)]
		tempDir = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
		destTile = [(x+1, y), (x+1, y), (x, y-1), (x, y-1)]
		destDir = [Direction.LEFT, Direction.RIGHT]

		for i in range (2):
			pos = self.calcPos(tempPos[i][0], tempPos[i][1])
			right = True
			left = True
			if gameboard.are_bullets_at_tile(pos[0], pos[1]):				#see if theres a bullet at that point
				for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:		#goes through all the bullets on that tile
					if b.direction == tempDir[i]:						#if the bullet is coming towards me
						if player.direction == destDir[0] or player.direction == destDir[1]:				#if the player is facing left/right
							right = not self.bulletsAround(gameboard, destDir[1], destTile[i][0], destTile[i][1])
							left = not self.bulletsAround(gameboard, destDir[0], x-1, y)
							#print(left, right)
							if not right and not left:
								if randint(0,1) == 0:
									temp = self.calcPos(x-1, y)
									temp2 = {temp[0], temp[1]}
									if temp2 in self.turret_cells:
										return Move.FACE_RIGHT
									return Move.FACE_LEFT
								else:
									temp = self.calcPos(x+1, y)
									temp2 = {temp[0], temp[1]}
									if temp2 in self.turret_cells:
										return Move.FACE_LEFT
									return Move.FACE_RIGHT
							elif not right and player.direction == Direction.RIGHT: 
								return Move.FACE_LEFT
							elif not left and player.direction == Direction.LEFT:
								return Move.FACE_RIGHT
							return Move.FORWARD								#if so, then move forward
						else:
							if gameboard.wall_at_tile[destTile[i][0]][destTile[i][1]]:
								return Move.FACE_LEFT
							if self.bulletsAround(gameboard, Direction.RIGHT, destTile[i][0], destTile[i][1]):
								return Move.FACE_LEFT
							return Move.FACE_RIGHT						#if not, then roate left/right

		tempPos = [(x+2, y), (x-2, y)]
		tempDir = [Direction.LEFT, Direction.RIGHT]
		destTile = [(x, y-1), (x, y-1)]
		destDir = [Direction.UP, Direction.DOWN]
		for i in range (2):
			pos = self.calcPos(tempPos[i][0], tempPos[i][1])
			up = True
			down = True
			if gameboard.are_bullets_at_tile(pos[0], pos[1]):				#see if theres a bullet at that point
				for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:		#goes through all the bullets on that tile
					if b.direction == tempDir[i]:						#if the bullet is coming towards me
						if player.direction == destDir[0] or player.direction == destDir[1]:				#if the player is facing left/right
							up = not self.bulletsAround(gameboard, destDir[1], destTile[i][0], destTile[i][1])
							down = not self.bulletsAround(gameboard, destDir[0], x, y+1)
							#print(up, down)
							if not up and not down:
								if randint(0,1) == 0:
									temp = self.calcPos(x, y-1)
									temp2 = {temp[0], temp[1]}
									if temp2 in self.turret_cells:
										return Move.FACE_DOWN
									return Move.FACE_UP
								else:
									temp = self.calcPos(x, y+1)
									temp2 = {temp[0], temp[1]}
									if temp2 in self.turret_cells:
										return Move.FACE_UP
									return Move.FACE_DOWN
							elif not up and player.direction == Direction.UP: 
								return Move.FACE_DOWN
							elif not down and player.direction == Direction.DOWN:
								return Move.FACE_UP
							return Move.FORWARD								#if so, then move forward
						else:
							if gameboard.wall_at_tile[destTile[i][0]][destTile[i][1]]:
								return Move.FACE_DOWN
							if self.bulletsAround(gameboard, Direction.UP, destTile[i][0], destTile[i][1]):
								return Move.FACE_DOWN
							return Move.FACE_UP						#if not, then roate left/right
	
		return Move.NONE

	def bulletsAround(self, gameboard, direction, x, y):
		if direction == Direction.UP:
			tempPos = [(x, y-1), (x+1, y), (x-1, y)]
			tempDir = [Direction.DOWN, Direction.LEFT, Direction.RIGHT]
		elif direction == Direction.DOWN:
			tempPos = [(x, y+1), (x+1, y), (x-1, y)]
			tempDir = [Direction.UP, Direction.LEFT, Direction.RIGHT]
		elif direction == Direction.LEFT:
			tempPos = [(x-1, y), (x, y+1), (x, y-1)]
			tempDir = [Direction.RIGHT, Direction.UP, Direction.DOWN]
		else:
			tempPos = [(x+1, y), (x, y+1), (x, y-1)]
			tempDir = [Direction.LEFT, Direction.UP, Direction.DOWN]
		for i in range(len(tempPos)):
			pos = self.calcPos(tempPos[i][0], tempPos[i][1])
			if gameboard.are_bullets_at_tile(pos[0], pos[1]):
				for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:
					if b.direction == tempDir[i]:
						return True
		return False