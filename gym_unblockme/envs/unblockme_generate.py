import numpy as np

# BOARD EXAMPLE
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


# Difficulty is the number of block other than the Red one (less or equal)
# we insert alternating a vertical and an horizontal one
# DISCLAIMER: There are no guarantee that the generated board is solvable,
# although if the difficulty is less than 5 is very likely 
def generate (width, height, difficulty = 1):

	matrix = np.zeros([width, height])
	goal = [0, 0]

	# Select the red block and goal position
	red_pos = np.random.randint(width)
	side    = np.random.randint(2)

	if side == 0:
		matrix[red_pos, :2] = [1,1]
		goal = [red_pos, height-1]
	else:
		matrix[red_pos,-2:] = [1,1]
		goal = [red_pos, 0]

	vertical = True
	for _ in range(difficulty):
		#adding block
		inserted = False

		if vertical: #vertical block
			x_pos = np.random.randint(width-1)
			y_pos = np.random.randint(height)
			# we insert the block only if the cells are free
			if (matrix[x_pos:x_pos+2,  y_pos] == [0,0]).all():
				matrix[x_pos:x_pos+2,  y_pos] = [3,3]
				inserted = True
		
		else: #horizontal block
			x_pos = np.random.randint(width-1)
			y_pos = np.random.randint(height-1)

			# we don't want to insert horizontal blocks in the 
			# line of the red block
			if x_pos == red_pos:
				x_pos += 1

			# we insert the block only if the cells are free
			if (matrix[x_pos,  y_pos:y_pos+2] == [0,0]).all():
				matrix[x_pos,  y_pos:y_pos+2] = [2,2]
				inserted = True

		if inserted:
			vertical = not vertical


	return matrix.astype(int), goal


if __name__ == "__main__":

	import unblockme_class as cl
	import unblockme_render as renderer
	import time

	matrix, goal = generate(5,5, difficulty = 5)
	game = cl.unblock_me(matrix, goal)
	game.print()
	renderer.render_unblockme(game)
	time.sleep(5)
