
import numpy as np

# Unblock Me class

def get_example():
	## Example matrix input
	matrix_input = np.array(
			[  [0, 2, 2, 0],
			   [1, 1, 0, 3],
			   [0, 0, 0, 3],
			   [2, 2, 0, 0]
			])

	target_input = [1,3]
	# 0: Empty
	# 1: Red Block
	# 2: Horizontal Blocks
	# 3: Vertical Blocks

	return matrix_input, target_input


class unblock_me:

	# Initialization
	## Input Space: W x H x 4
	# (Semplification: Only use length 2 blocks)
	# (Semplification2: Assume Red Block is Horizontal) <--
	#
	# Layer 0: Target Position
	# Layer 1: Red Block
	# Layer 2: Horizontal Blocks
	# Layer 3: Vertical Blocks 
	def __init__ (self, matrix, goal):

		self.goal = goal
		goal_x, goal_y = self.goal
		self.shape = matrix.shape + (4,)
		self.internal_state = np.zeros(self.shape)

		self.internal_state[goal_x,goal_y,0] = 1 #Target Position

		for i in range(1,4):
			self.internal_state[:,:,i] = (matrix == i).astype(int)

		self.num_blocks = np.sum((self.internal_state[:,:,1:] != 0).astype(int))/2

	def __is_valid (self, x,y):

		return  x >= 0 and x < self.shape[0] and \
				y >= 0 and y < self.shape[1]

	def get_block_listed(self):
		r = np.nonzero(self.internal_state[:,:,0])
		b = [i for i in zip(r[0],r[1])]
		state = b
		for i in range(1,3):
			r = np.nonzero(self.internal_state[:, :, i])
			b = [i for i in zip(r[0],r[1])]
			state += (b)

		# for the vertical blocks we transpose to have the coordinates in the right order
		r = np.nonzero(np.transpose(self.internal_state[:, :, 3]))
		b = [i for i in zip(r[1], r[0])]
		state += (b)

		r = np.array(state).flatten()

		return r

	def is_solved(self):

		goal_x, goal_y = self.goal
		goal_cell = self.internal_state[goal_x, goal_y,:]
		return (goal_cell == [1,1,0,0]).all()

	def print(self):
		matrix = np.copy(self.internal_state[:,:,0])
		for i in range(1,4):
			matrix += (self.internal_state[:,:,i] == 1).astype(int)*(i+1)

		print(matrix)

	# Valid only if (x,y) targets a block (Horizontal, Vertical or Red)
	# Valid only if the direction is empty 
	#
	# (X,Y) Coordinates where (0,0) is the top left corner
	#
	# DIR (Depends on the type of block)
	# 0: up, left
	# 1: down, right
	#
	# Return: True if the move is valid, False instead
	def __act(self, x, y, dir):
		cell = self.internal_state[x,y,1:]

		# No block selected
		if (cell == 0).all():
			return False

		# Check if in the selected cell there is only 1 block
		# If not then the board is in an inconsistent state and we raise an expection
		selected_block = np.where(cell == 1)[0]
		if len(selected_block) > 1:
			print("Coordinates: " + str((x,y)))
			print("Cell content: " + self.internal_state[x,y,:])
			raise Exception("Inconsistent state of the board")

		selected_block = selected_block[0]

		# Target Direction to move
		shift_x = 0; shift_y = 0

		# If is the Red or Horizontal Block than try to move (left, right)
		# (because of Semplification2)
		if selected_block in [0,1]:

			if dir == 0: # move left
				shift_x = 0; shift_y = -1

			else: # move right
				shift_x = 0; shift_y = +1

		# Vertical Block
		else: 
			if dir == 0: # move up
				shift_x = -1; shift_y = 0

			else: # move down
				shift_x = +1; shift_y = 0
				
		if not self.__is_valid(x + shift_x, y + shift_y):
			return False

		# if the target cell is occupied, it could mean that we
		# are selecting the other part of the block
		if (self.internal_state[x + shift_x, y + shift_y,1:] == 1).any():
			
			# if it is a different block, the move is Invalid
			if not (self.internal_state[x + shift_x, y + shift_y,1:] == cell).all():
				return False

			# if also the second cell is occupied the move is invalid
			if not self.__is_valid(x + 2*shift_x, y + 2*shift_y):
				return False
			if (self.internal_state[x + 2*shift_x, y + 2*shift_y, 1:] == 1).any():
				return False

			# Move the tile and free the space
			self.internal_state[x + 2*shift_x, y + 2*shift_y,1:] = cell
			self.internal_state[x            , y            ,1:] = [0,0,0]

		else:

			# Move the tile and free the space
			self.internal_state[x + shift_x, y + shift_y,1:] = cell
			self.internal_state[x - shift_x, y - shift_y,1:] = [0,0,0]

		# if we reached this point the move as been succesful 
		return True

	def act(self, action):
		if len(action) != 3:
			raise Exception("Non valid action")

		if not (action[:2] < self.shape[:2]).all(): 
			raise Exception("Non valid action")

		if action[2] not in [0,1]:
			raise Exception("Non valid action")

		return self.__act(action[0], action[1], action[2])

if __name__ == "__main__":

    #from unblockme_gym import *
	matrix, goal = get_example()
	game = unblock_me(matrix, goal)
	game.print()
	print(game.num_blocks)
	print(game.get_block_listed())