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
							10:Move.FORWARD}
		self.checkOffsets = [(0,2), (0,1), (0,-1), (0,-2),
						(-2,0),(-1,0),(1,0), (2, 0)]
		self.init = False
		pass

	def get_move(self, gameboard, player, opponent):
		if self.init == False:
			self.init1(gameboard, player)
		else:
			pass

		block1 = True
		myDir = self.intDir[player.direction]
		result = self.colDet(gameboard, player)
		if result != -1:
			return result
		#print (myDir)

		#if player.x != 3:
			#return Move.FORWARD
		#if len(gameboard.bullets) > 0:
		#	print(gameboard.bullets[0].direction)
		#	print(gameboard.bullets[0].shooter)
		#	print(gameboard.bullets[0].x, gameboard.bullets[0].y)
		return Move.NONE

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
							print(left, right)
							if not right and not left:
								#if b.direction == Direction.DOWN:
									#return Move.FACE_DOWN
								#return Move.FACE_UP
								if randint(0,1) == 0:
									return Move.FACE_LEFT
								else:
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
							print("LEFT", self.bulletsAround(gameboard, Direction.LEFT, 
								destTile[i][0], destTile[i][1]))
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
							print(up, down)
							if not up and not down:
								# if b.direction == Direction.RIGHT:
								# 	return Move.FACE_RIGHT
								# return Move.FACE_LEFT
								if randint(0,1) == 0:
									return Move.FACE_UP
								else:
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
		

		# pos = self.calcPos(x, y+2)
		# if gameboard.are_bullets_at_tile(pos[0], pos[1]):				#see if theres a bullet at that point
		# 	for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:		#goes through all the bullets on that tile
		# 		if b.direction == Direction.UP:						#if the bullet is coming towards me
		# 			if self.intDir[player.direction] > 1:				#if the player is facing left/right
		# 				if gameboard.wall_at_tile[x+1][y]:
		# 					return Move.FACE_RIGHT
		# 				elif self.bulletsAround(gameboard, Direction.LEFT, x+1, y):
		# 					return Move.FACE_RIGHT
		# 				return Move.FORWARD								#if so, then move forward
		# 			else:
		# 				if gameboard.wall_at_tile[x+1][y]:
		# 					return Move.FACE_RIGHT
		# 				elif self.bulletsAround(gameboard, Direction.LEFT, x+1, y):
		# 					return Move.FACE_RIGHT
		# 				print("LEFT", self.bulletsAround(gameboard, Direction.LEFT, x+1, y))
		# 				return Move.FACE_LEFT						#if not, then roate left/right
		# pos = self.calcPos(x, y-2)
		# if gameboard.are_bullets_at_tile(pos[0], pos[1]):				
		# 	for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:	
		# 		if b.direction == Direction.DOWN:						
		# 			if self.intDir[player.direction] > 1:				
		# 				return Move.FORWARD						
		# 			else:
		# 				if gameboard.wall_at_tile[x+1][y]:
		# 					return Move.FACE_RIGHT
		# 				elif self.bulletsAround(gameboard, Direction.LEFT, x+1, y):
		# 					return Move.FACE_RIGHT
		# 				return Move.FACE_LEFT						
		# pos = self.calcPos(x+2, y)
		# if gameboard.are_bullets_at_tile(pos[0], pos[1]):				
		# 	for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:	
		# 		if b.direction == Direction.LEFT:
		# 			if self.intDir[player.direction] < 2:
		# 				return Move.FORWARD
		# 			else:						
		# 				if gameboard.wall_at_tile[x][y-1]:
		# 					return Move.FACE_DOWN
		# 				elif self.bulletsAround(gameboard, Direction.UP, x, y-1):
		# 					return Move.FACE_DOWN
		# 				return Move.FACE_UP
		# pos = self.calcPos(x-2, y)
		# if gameboard.are_bullets_at_tile(pos[0], pos[1]):				
		# 	for b in gameboard.bullets_at_tile[pos[0]][pos[1]]:	
		# 		if b.direction == Direction.RIGHT:
		# 			if self.intDir[player.direction] < 2:				
		# 				return Move.FORWARD
		# 			else:
		# 				if gameboard.wall_at_tile[x][y-1]:
		# 					return Move.FACE_DOWN
		# 				elif self.bulletsAround(gameboard, Direction.UP, x, y-1):
		# 					return Move.FACE_DOWN
		# 				return Move.FACE_UP		

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
			


	# def colDet1(self, gameboard, player, x, y):

	# 	pos = self.calcPos(x, y+2)
	# 	if gameboard.areBulletsAtTile(pos[0], pos[1]):				#see if theres a bullet at that point
	# 		for b in gameboard.getBulletsAtTile(pos[0], pos[1]):	#goes through all the bullets on that tile
	# 			if b.direction == Direction.UP:						#if the bullet is coming towards me
	# 				if intDir[player.direction] > 1:				#if the player is facing left/right
	# 					return Move.FORWARD								#if so, then move forward
	# 				else:
	# 					return Move.FACE_LEFT						#if not, then roate left/right

	# 	pos = self.calcPos(x, y+1)
	# 	if gameboard.areBulletsAtTile(pos[0], pos[1]):
	# 		for b in gameboard.getBulletsAtTile(pos[0], pos[1]):
	# 			if b.direction == Direction.UP:
	# 				if intDir[player.direction] > 1:
	# 					return Move.FORWARD


	# 	for couple in self.checkOffsets:
	# 		if gameboard.areBulletsAtTile(x+couple[0], y+couple[1]):
	# 			pass


	# def oldColDet(self):


	# 	for b in gameboard.bullets:
	# 		if b.x == player.x:

	# 			if block1 and abs(b.y-player.y) == 1:
	# 				if self.intDir[player.direction] > 1:
	# 					return Move.FORWARD
	# 				#else:
	# 					#your ded

	# 			if abs(b.y-player.y) == 2:
	# 				direct = self.opponentDirX(player, opponent)
	# 				if direct == -1:
	# 					return Move.FORWARD
	# 				else:
	# 					return self.intComDir[direct]
	# 				#if self.intDir[player.direction] > 1:
	# 				#	return self.comDir[player.direction]
	# 			#if abs(b.y - player.y) == 2:
	# 				#if b.direction == 

