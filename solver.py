import sys
import os
import random
import time

### I/O HELPERS ###

def type_writer(string, t=0.1):
	for letter in string:	
		print(letter, end="")
		sys.stdout.flush()
		time.sleep(random.uniform(0, t))
	print("")

def clean_type_writer(string, t=0.03):
	for letter in string:
		print(letter, end="")
		sys.stdout.flush()
		time.sleep(t)
	print("")

def print_board(board):
	rows = []
	size = len(board)
	line = "|" + "-" * (size * 3 + size - 1) + "|"
	for row in board:
		string = "|"
		for num in row:
			string += " " + str(num) + " |"
		rows.append(string)

	print(line)
	for r in rows:
		print(r)
		print(line)

def invalid(inp):
	if len(inp) != 9:
		return True
	reduced = [x for x in inp if x != '0']
	if len(reduced) != len(set(reduced)):
		return True
	for elem in inp:
		if int(elem) not in range(10):
			return True
	return False

def start():
	os.system("clear")
	h = open("header.txt", "r")
	text = h.read()
	clean_type_writer(text, 0.002)
	rows = range(1,10)
	inputs = []
	for row in rows:
		print("Enter row " + str(row), "\nEnter 0 where there is a missing number")
		inp = input()
		while (invalid(inp)):
			type_writer("\nInvalid input try again")
			print("Enter row " + str(row))
			inp = input()
		inputs.append(inp)
	return inputs

# 9 x 9 array
# we want to be able to extract row, column, and quartile quickly
# start with a huge array with -1 for blanks

### LOGIC HELPERS ###

def get_row(board, pos):
	return board[pos]

def check_row(board, pos):
	return set(get_row(board, pos)) == set([1,2,3,4,5,6,7,8,9])

def get_column(board, pos):
	return [row[pos] for row in board]

def check_column(board, pos):
	return set(get_column(board, pos)) == set([1,2,3,4,5,6,7,8,9])

def get_quartile(board, quartile_num): 
	selections = [[0,1,2],[3,4,5],[6,7,8]]
	
	# for offset into the rows
	mod = quartile_num % 3
	secondary = selections[mod]
	
	# which rows to select
	if quartile_num < 3:
		sector = 0
	elif quartile_num > 5:
		sector = 2
	else:
		sector = 1
	primary = selections[sector]

	result = []
	for p in primary:
		result.extend([board[p][offset] for offset in secondary])
	return result

def check_quartile(board, quartile_num):
	return set(get_quartile(board, quartile_num)) == set([1,2,3,4,5,6,7,8,9])

def valid_board(board):
	for i in range(9):
		if check_row(board, i) == False:
			#print(get_row(board, i))
			return False
		if check_column(board, i) == False:
			#print(get_column(board, i))
			return False
		if check_quartile(board, i) == False:
			#print(get_quartile(board, i))
			return False
	return True

def quartile_num_from_pos(row, column):
	selections = [[0,1,2],[3,4,5],[6,7,8]]
	if row < 3:
		sector = 0
	elif row > 5:
		sector = 2
	else:
		sector = 1

	if column < 3:
		offset = 0
	elif column > 5:
		offset = 2
	else:
		offset = 1

	return selections[sector][offset]

# for each position, if empty find all numbers that can be
def get_posibilites(board, row, column):
	row_options = get_row(board, row)
	column_options = get_column(board, column)

	quartile_num = quartile_num_from_pos(row, column)
	quartile_options = get_quartile(board, quartile_num)

	everything_it_cant_be = set(row_options + column_options + quartile_options)
	return [x for x in range(1,10) if x not in everything_it_cant_be]

def update_board(board):
	tag = False
	for i in range(9):
		for j in range(9):
			if board[i][j] == 0: # is blank
				posibilites = get_posibilites(board, i, j)
				if len(posibilites) == 1:
					board[i][j] = posibilites[0]
					tag = True
				elif len(posibilites) == 0:
					# unsolveable
					return
	return tag

### SOLVER ###

def solve(board):
	# start timer
	start = time.time()
	while(valid_board(board) == False):
		updated = update_board(board)
		if updated == None:
			return "cant solve"
		if updated == False:
			#brute force time
			return " too HARD..."
		if time.time() - start > 60 * 3:
			return "TIMEOUT"
	# end timer
	end = time.time()
	elapsed = (end - start) // 1
	return elapsed

def brute_force(board):
	tried_boards = []
	# get all possibilites for each square
	possibilites_grid = []
	
	
	new_board = fill_board(board)
	tried_boards.append(new_board)

	while(valid_board(board) == False):
		new_board = fill_board(board)



### MAIN ### 
if __name__ == "__main__":
	inputs = start()
	board = []
	[board.append([int(x) for x in inp]) for inp in inputs]
	print_board(board)

	# ask if this looks correct
	type_writer("Is This Correct?")
	response = input()

	while response.lower() not in ["yup", "yes", "yeah", "ye", "y", "yea", "yep", "yee", "yeee", "yus", "yas"]:
		# add regex

		type_writer("Which Row is Incorrect [1-9]")
		
		response_row = input()
		# verify valid input
		try:
			response_row = int(response_row)
			if response_row not in list(range(1,10)):
				type_writer("Not a valid row number")
				continue
		except:
			type_writer("Not a valid row number")
			continue
		#

		type_writer("Re-type Row " + str(response_row))
		inp = input()
		#verify 
		while (invalid(inp)):
			type_writer("\nInvalid input try again")
			print("Enter row " + response_row)
			inp = input()
		#

		board[response_row - 1] = [int(x) for x in inp]
		print_board(board)

		# ask if this looks correct
		type_writer("Is This Correct?")
		response = input()


	os.system("clear")
	type_writer("starting...")
	elapsed = solve(board)

	if type(elapsed) == str:
		print(elapsed)
	else:
		print("\nWe Solved It!")
		print_board(board)
		print("\nIt took " + str(elapsed) + " seconds")








