import tkinter as tk
from tkinter import messagebox as mb
import os
import random
from datetime import datetime

choiceOfDimension = 0
solutions = []
solutions_to_show = []

def construct_game_gui():

	game = tk.Tk()
	game.title("N Queens Puzzle")

	first_page = tk.Frame(game)
	second_page = tk.Frame(game)

	menu = tk.Menu(game)
	game.config(menu=menu)
	gamemenu = tk.Menu(menu)
	menu.add_cascade(label="Options", menu=gamemenu)

	dimensions = [("4x4"), ("5x5"), ("6x6"), ("7x7"), ("8x8")]

	def clear_frame(frame):
		for widget in frame.winfo_children():
			widget.destroy()

		frame.pack_forget()

	def construct_second_page():
		clear_frame(first_page)

		get_solution()
		input_solution = [0 for x in range(choiceOfDimension + 4)]

		print(input_solution)

		def checkSolution():
			result = ""
			global solutions, solutions_to_show
			print("input_solution = ", input_solution)
			if (str(input_solution) in solutions or str(input_solution.reverse()) in solutions):
				result = "Congratulations! You Have Successfully Solved the Puzzle.\nHere are the possible or some of the possible solutions for given 'n'\n"
				for i in range(len(solutions_to_show)):
					result += solutions_to_show[i] + "\n"
				
			else:
				result = "Sorry! Incorrect Solution."

			mb.showinfo("Results", result)
			NewGame()

		def checkered():

			def checkOtherPositions(x, y, dimension):
				
				def checkForRow():
					i = x
					for j in range(dimension):
						state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
						if (state == "normal"):
							return False
					return True

				def checkForColumn():
					j = y
					for i in range(dimension):
						state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
						if (state == "normal"):
							return False
					return True

				def checkForSimpleDiagonal():
					a = x
					b = y

					i=a
					j=b
					if (a==0):
						while(i<dimension and j<dimension):
							state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
							if (state == "normal"):
								return False
							i += 1
							j += 1

					elif (a==3):
						while(i>=0 and j>=0):
							state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
							if (state == "normal"):
								return False
							i -= 1
							j -= 1

					else:
						while (i>=0 and j>=0):
							state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
							if (state == "normal"):
								return False
							i -= 1
							j -= 1

						i = a
						j = b

						while(i<dimension and j<dimension):
							state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
							if (state == "normal"):
								return False
							i += 1
							j += 1

					return True

				def checkForCrossDiagonal():
					i = x
					j = y

					while(i<4 and j>=0):
						state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
						if (state == "normal"):
							return False
						i += 1
						j -= 1

					i = x
					j = y

					while (i>=0 and j<4):
						state = (canvas.itemconfigure(imageIDs[i][j]))['state'][4]
						if (state == "normal"):
							return False
						i -= 1
						j += 1

					return True

				if (checkForRow() and checkForColumn() and checkForSimpleDiagonal() and checkForCrossDiagonal()):
					return True
				
				return False    

			def onTap(eventorigin):
				x = eventorigin.y//line_distance
				y = eventorigin.x//line_distance

				state = (canvas.itemconfigure(imageIDs[x][y]))['state'][4]

				if (state == "hidden"):
					if (checkOtherPositions(x, y, dimension) == False):
						mb.showinfo("Info", "Cannot place a queen here!")
					else:
						canvas.itemconfigure(imageIDs[x][y], state="normal")
						print(x,y)
						input_solution[x] = y
				elif (state == "normal"):
					canvas.itemconfigure(imageIDs[x][y], state="hidden")
					input_solution[x] = 0

				print(input_solution)

			img = tk.PhotoImage(file="queen.ppm")
			dimension = choiceOfDimension+4
			canvas_width = (dimension)*100
			canvas_height = (dimension)*100
			line_distance = 100

			if (choiceOfDimension == 4):
				img = tk.PhotoImage(file="queen_small.ppm")
				canvas_width = canvas_width//2
				canvas_height = canvas_height//2
				line_distance = line_distance//2
				
			h = line_distance//2

			canvas = tk.Canvas(second_page, width=canvas_width, height=canvas_height, bd=10, relief=tk.GROOVE)

			canvas.pack(anchor=tk.E, side="left", fill="both", expand=True)

			canvas.bind("<Button 1>", onTap)

			imageIDs = [[0 for x in range(dimension)] for x in range(dimension)] 

			for x in range(line_distance, canvas_width, line_distance):
				canvas.create_line(x, 0, x, canvas_width, fill = "#000000")

			for y in range(line_distance, canvas_height, line_distance):
				canvas.create_line(0, y, canvas_height, y, fill="#000000")

			for y in range(0, canvas_height, line_distance): 
				for x in range(0, canvas_width, line_distance):
					if ((y//line_distance)%2==0):
						if ((x//line_distance)%2==0):
							canvas.create_rectangle(x, y, x+line_distance, y+line_distance, fill="#DEB887")
					else:
						if ((x//line_distance)%2!=0):
							canvas.create_rectangle(x, y, x+line_distance, y+line_distance, fill="#DEB887")
					
					item = canvas.create_image(x+h, y+h, image=img, state="hidden")
					imageIDs[y//line_distance][x//line_distance] = item
					game.one = img

		gamemenu.delete(0, 'end')
		gamemenu.add_command(label="New Game", command=NewGame)
		gamemenu.add_command(label="Restart Game", command=RestartGame)
		gamemenu.add_command(label="Show Solutions", command=ShowSolution)

		gamemenu.add_separator()

		gamemenu.add_command(label="Exit", command=Exit)

		tk.Label(second_page, text="Note: ", fg="red", font="Verdana 16 bold underline").pack(anchor=tk.W)  
		tk.Message(second_page, text="A chess queen moves vertically, horizontally, or diagonally.\nTap on the block in the chessboard to place a queen there.", width=1000).pack(anchor=tk.N, side=tk.LEFT)

		tk.Button(second_page, text="Submit", font="Times 14 bold", fg="blue", bg="yellow", command=checkSolution).pack(side=tk.BOTTOM)

		checkered()
		second_page.pack()

	def construct_first_page():
		first_page.pack()

		gamemenu.delete(0, 'end')

		gamemenu.add_command(label="New Game", command=NewGame)
		gamemenu.add_separator()

		gamemenu.add_command(label="Exit", command=Exit)

		heading_label = tk.Label(first_page, text="Welcome to N Queens Puzzle!", fg="red", bg="yellow", font="Verdana 24 bold italic", pady=5, padx=5)
		heading_label.pack()

		problem_stmnt_frame = tk.Frame(first_page, padx=50, pady=50)
		problem_stmnt_frame.pack()

		problem_statement = "To place N-Queens on an NxN chessboard such that no two queens attack each other."

		problem_statement_label = tk.Label(problem_stmnt_frame, text="Problem Statement:", padx=10, font="Helvetica 16 bold underline", justify=tk.LEFT)
		problem_statement_label.pack(side="left")

		msg = tk.Message(problem_stmnt_frame, text=problem_statement)
		msg.config(fg="white", bg="grey", font=("times", 14, "italic"), width=1000, justify=tk.LEFT)
		msg.pack(side="left")

		v = tk.IntVar()

		tk.Label(first_page, text="Choose chessboard dimension: ", justify=tk.LEFT, padx=25).pack(anchor=tk.W)

		def SelectChoice():
			global choiceOfDimension
			choiceOfDimension = v.get()
			print("choice_of_dimenstion = ", v.get())          
		
		for val, dimension in enumerate(dimensions):
			tk.Radiobutton(first_page, text=dimension, padx=30, variable=v, command=SelectChoice, value=val).pack(anchor=tk.W)

		start_button = tk.Button(first_page, text="START",command=construct_second_page)
		start_button.pack()

	def NewGame():
		if (first_page.winfo_ismapped()):
			clear_frame(first_page)
		elif (second_page.winfo_ismapped()):
			clear_frame(second_page)

		global choiceOfDimension, solutions, solutions_to_show
		choiceOfDimension=0
		solutions.clear()
		solutions_to_show.clear()

		construct_first_page()

	def RestartGame():
		clear_frame(second_page)
		global solutions
		solutions=0
		construct_second_page()

	def ShowSolution():
		global solutions_to_show
		solution = "Here are the possible or some of the possible solutions for given 'n'\n"
		for i in range(len(solutions_to_show)):
			solution += solutions_to_show[i] + "\n"
		mb.showinfo("Solutions", solution)

	def Exit():
		if mb.askyesno(title="Verify", message="Do you really want to quit ?"):
			mb.showinfo(title="Info", message="Thank You! I hope you had a good time.")
		else:
			mb.showinfo(title="Info", message="Let's play!")
		game.quit()


	construct_first_page()

	game.mainloop()

def get_solution():

	def can_be_extended_to_solution(perm):
		i = len(perm) - 1
		for j in range(i):
			if i - j == abs(perm[i] - perm[j]):
				return False
		return True

	def extend(perm, n):
		if len(perm) == n:
			solutions.append(str(perm))
			perm = []
			return

		for k in range(n):
			if k not in perm:
				perm.append(k)

				if can_be_extended_to_solution(perm):
					extend(perm, n)

				perm.pop()


	global solutions, choiceOfDimension, solutions_to_show

	n = choiceOfDimension + 4

	numberOfSolutionsToShow = 0
	if (n == 4):
		numberOfSolutionsToShow += 2
	else:
		numberOfSolutionsToShow += 5

	extend(perm = [], n = n)

	print("Total number of solutions: %d"%(len(solutions)))
	
	if (n==4):
		solutions_to_show.extend(solutions)
	else:
		random.seed(datetime.now())
		while(numberOfSolutionsToShow):
			solutions_to_show.append(random.choice(solutions))
			numberOfSolutionsToShow -= 1

	print("solutions_to_show = ", solutions_to_show)
	
if __name__ == '__main__':
	construct_game_gui()