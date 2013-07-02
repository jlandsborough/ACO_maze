
from Tkinter import *
from Ant import Ant
from Location import Location
import time
import csv

DEBUG = 0

######  GLOBAL VARIABLES
MAP_WIDTH = 15          #Width of map/maze
MAP_HEIGHT = 15         #Height of map/maze
SQUARE_SIZE = 30        #Size of each box in pixels
PLVL_DEPLETE = 0.1        #depletion rate for pheromones per iteration
PLVL_ADD = 2000 #5 * MAP_WIDTH * MAP_HEIGHT



#ant gif: http://openclipart.org/detail/66/ant-by-andy
#home gif: http://openclipart.org/image/20px/svg_to_png/30805/go-home.png
#food gif: http://openclipart.org/image/20px/svg_to_png/9079/Gerald_G_Fast_Food_Lunch_Dinner_(FF_Menu)_6.png
#ant food gif: modified ant gif




#GUI Class
class ACOworld_tk():
        def __init__(self):
                ###variables
                self.delay = 300 #delay between iterations
		self.n_iterations = 0 #number of iterations
		self.stockpile = 0
		self.pause = 1
		self.home = 0
		self.food = 0
                self.ant_list = [] #list of ants
                self.map = [ [Location() for x in xrange(MAP_HEIGHT)] for x in range(MAP_WIDTH)] #map

		#set map locations to x,y coordinates
		for i in xrange(MAP_WIDTH):
			for j in xrange(MAP_HEIGHT):
				self.map[i][j].set_location(i, j)


		
                #default walls
		self.default_map()
		#default ants
                self.default_ants()

		###GUI setup
                self.root = Tk()
                self.root.wm_title("ACO world")
                self.root.geometry(str((MAP_WIDTH*SQUARE_SIZE)+120) + "x" + str((MAP_HEIGHT*SQUARE_SIZE)+50) + "+100+100") #window size

                #top frame
                self.topframe = Frame(self.root, height = 100)
                self.topframe.grid(row = 0, column = 1)

                #Button pause/resume
                self.button_pause = Button(self.root, text="Resume", command=self.pause_resume)
                self.button_pause.grid(row = 0, column = 0)

                #left frame
                self.sideframe = Frame(self.root)
                self.sideframe.grid(row = 1, column = 0, sticky = N)

                #label on top frame
                self.labeltop = Label(self.topframe, text="Iteration: 0")
                self.labeltop.pack(side = LEFT)

		
		#label for speed/delay of iterations                
		self.label_speedlabel = Label(self.sideframe, text="Iteration Delay:")
                self.label_speedlabel.pack(side = TOP)
                self.label_speed = Label(self.sideframe, text=str(self.delay)+"ms")
                self.label_speed.pack()


                #button speed up
                self.button_upspeed = Button(self.sideframe, text="Speed up   ", command=self.speed_up)
                self.button_upspeed.pack()

                #button slow down
                self.button_downspeed = Button(self.sideframe, text="Slow down", command=self.slow_down)
                self.button_downspeed.pack()

                #button add ant
                self.blanklabel = Label(self.sideframe, text=" ")
                self.blanklabel.pack()
                self.button_addant = Button(self.sideframe, text="Add ant", command=self.add_ant)
                self.button_addant.pack()

                #button kill ant
                self.blanklabel = Label(self.sideframe, text=" ")
                self.blanklabel.pack()
                self.button_killant = Button(self.sideframe, text="Kill ant", command=self.kill_ant)
                self.button_killant.pack()

                #button clear walls
                self.blanklabel2 = Label(self.sideframe, text =" ")
                self.blanklabel2.pack()
                self.button_clearwalls = Button(self.sideframe, text="Clear walls", command=self.clear_walls)
                self.button_clearwalls.pack()

                #label pheromone level
                self.blanklabel = Label(self.sideframe, text =" ")
                self.blanklabel.pack()
                self.label_paddlabel = Label(self.sideframe, text = "Pheromone drop:")
                self.label_paddlabel.pack()
                self.label_padd = Label(self.sideframe, text=str(PLVL_ADD) + "/trip^2")
                self.label_padd.pack()
                
                #Canvas/Map
                self.cmap = Canvas(self.root, width = MAP_WIDTH * SQUARE_SIZE, height = MAP_HEIGHT * SQUARE_SIZE, bg = "white")
                self.cmap.grid(row = 1, column = 1)
                self.cmap.bind("<Button 1>", self.click_map)

		### Images
		#NOTE: you will need to change resolution of image if 
		#	SQUARE_SIZE is smaller than either vertical/horizontal resolution
		#ant gif
		self.antgif = PhotoImage(file = "gui_images/20px_Andy_ant.gif")  #20x20pixel gif of ant
		self.homegif = PhotoImage(file = "gui_images/20px_home.gif")  #20x20pixel gif of ant
		self.foodgif = PhotoImage(file = "gui_images/20px_burger.gif")  #20x20pixel gif of ant
		self.antfoodgif = PhotoImage(file = "gui_images/20px_Andy_ant_food.gif") #20x20pixel of ant with "food"

		###Run iterations
                self.update()
                self.root.mainloop()

        def pause_resume(self):
                if self.pause == 1:
                        self.pause = 0
                        self.button_pause.config(text="Pause")
                else:
                        self.pause = 1
                        self.button_pause.config(text="Resume")

	def default_map(self):
                #default home
		#self.home = self.map[1][1]
                self.home = self.map[1][7]
		self.home.set_home()

                #default food
		#self.food = self.map[14][11]
		self.food = self.map[13][7]
                self.food.set_food_source()
                
		#self.map[2][2].increase_pheromone(.001)
		#self.map[3][2].increase_pheromone(10)
		#self.map[4][2].increase_pheromone(20)
		#self.map[5][2].increase_pheromone(40)
		#self.map[6][2].increase_pheromone(100)
		#self.map[7][2].increase_pheromone(200)


                #read walls from input file
                infile = open('walls.csv', "rb")
                reader = csv.reader(infile)
                
                j = 0
                for row in reader:
                        i = 0
                        for col in row:
                                 
                                if str(col) == str(1):
                                	self.map[i][j].set_blocked()
                                i = i + 1       
                        j = j + 1

		

	def default_ants(self):
		for i in xrange(20):
                        a = Ant(self.home.get_x(), self.home.get_y())
                        self.ant_list.append(a)
                        

        def speed_up(self):
                if self.delay > 100:
                        self.delay = self.delay - 100
                else:
                        self.delay = self.delay - 10
                if self.delay <= 0:
                        self.delay = 10
                self.label_speed.config(text=str(self.delay)+"ms")

        def slow_down(self):

                if self.delay > 90:
                        self.delay = self.delay + 100
                else:
                        self.delay = self.delay + 10
                self.label_speed.config(text=str(self.delay)+"ms")

        def add_ant(self):
                a = Ant(self.home.get_x(), self.home.get_y())
                self.ant_list.append(a)

        def kill_ant(self):
                if len(self.ant_list) > 0:
                        self.ant_list.reverse() #alternate between removing from front and end of list
                        self.ant_list.pop()

        def clear_walls(self):
                for i in xrange(MAP_WIDTH):
			for j in xrange(MAP_HEIGHT):
                                self.map[i][j].unset_blocked()
		self.clear_map()
		self.draw_map()
                
        def clear_map(self):
                self.cmap.delete(ALL)



        def draw_map(self):
                # Draw Horizontal lines
		for i in xrange(MAP_HEIGHT):
			self.cmap.create_line(0, i*SQUARE_SIZE, MAP_WIDTH*SQUARE_SIZE, i*SQUARE_SIZE, fill="grey")
                # Draw Vertial lines
		for i in xrange(MAP_WIDTH):
			self.cmap.create_line(i*SQUARE_SIZE, 0, i*SQUARE_SIZE, MAP_HEIGHT*SQUARE_SIZE, fill="grey")
                # Draw walls, food, and home
		for i in xrange(MAP_WIDTH):
			for j in xrange(MAP_HEIGHT):
                                # draw pheromone level
				plvl = self.map[i][j].get_pheromone()
				if plvl > 0 and plvl < 5:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="violet")
                                elif plvl >= 5 and plvl < 15:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="light blue")
                                elif plvl >= 15 and plvl < 35:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="light green")
                                elif plvl >= 35 and plvl < 75:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="yellow")
                                elif plvl >= 75 and plvl < 155:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="orange")
                                elif plvl >= 155:
                                        self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="red")
				if self.map[i][j].is_blocked() == 1:
					self.cmap.create_rectangle(i*SQUARE_SIZE, j*SQUARE_SIZE, (i+1)*SQUARE_SIZE, (j+1)*SQUARE_SIZE, fill="black")
                                        if DEBUG:
						print("FOUND WALL:" + str(i) + "," + str(j) + "\n")
				# Draw home
				if self.map[i][j].is_home():
                                        self.cmap.create_image(i*SQUARE_SIZE, j*SQUARE_SIZE, image=self.homegif, anchor=NW)
				# Draw food
				if self.map[i][j].is_food_source():
                                        self.cmap.create_image(i*SQUARE_SIZE, j*SQUARE_SIZE, image=self.foodgif, anchor=NW)
					
                # Draw ants
		for ant in self.ant_list:
			if ant.has_food():
                        	self.cmap.create_image(ant.get_x()*SQUARE_SIZE, ant.get_y()*SQUARE_SIZE, image=self.antfoodgif, anchor=NW)
			else:
                        	self.cmap.create_image(ant.get_x()*SQUARE_SIZE, ant.get_y()*SQUARE_SIZE, image=self.antgif, anchor=NW)
                

        def click_map(self, event):
		#convert from coordinates to array element row and column
		row = int(event.x/SQUARE_SIZE)
		column = int(event.y/SQUARE_SIZE)
		if self.map[row][column].is_blocked() == 1: 	#if blocked
			self.map[row][column].unset_blocked() 	# erase wall
		else:						#if not blocked
			self.map[row][column].set_blocked()	# build wall
		self.clear_map()				#clear map
		self.draw_map()					#re-draw map (with changes)


		if DEBUG:
			print("Block: " + str(row) + "," + str(column) + "\n")
                

        def update(self):
		if not self.pause:
                	self.clear_map() 	#clear map

                        # decrease pheromone level
                        for i in xrange(MAP_WIDTH):
                                for j in xrange(MAP_HEIGHT):
                                        self.map[i][j].decrease_pheromone(PLVL_DEPLETE)

			# Move ants
                	if self.n_iterations != 0:
                                for ant in self.ant_list:
                                        movelist = []
                                        antx = ant.get_x()
                                        anty = ant.get_y()

                                        prevx = ant.get_prev_x()
                                        prevy = ant.get_prev_y()
                                        #add possible moves to movelist
                                        #check move above (not blocked and within bounds of map)
                                        if anty -1 >= 0 and self.map[antx][anty - 1].is_blocked() == 0 and (prevx != antx or prevy != anty - 1):
                                                movelist.append(self.map[antx][anty - 1])
                                        #check move right (not blocked and within bounds of map)
                                        if antx + 1 < MAP_WIDTH and self.map[antx + 1][anty].is_blocked() == 0 and (prevx != antx + 1 or prevy != anty):
                                                movelist.append(self.map[antx + 1][anty])
                                        #check move below (not blocked and within bounds of map)
                                        if anty + 1 < MAP_HEIGHT and self.map[antx][anty + 1].is_blocked() == 0 and (prevx != antx or prevy != anty + 1):
                                                movelist.append(self.map[antx][anty + 1])
                                        #check move left (not blocked and within bounds of map)
                                        if antx - 1 >= 0 and self.map[antx - 1][anty].is_blocked() == 0 and (prevx != antx - 1 or prevy != anty):
                                                movelist.append(self.map[antx - 1][anty])

                                        #make move
                                        ant.move(movelist)

                                        antx = ant.get_x()
                                        anty = ant.get_y()

                                        #check if on food source
                                        if self.food.get_x() == antx and self.food.get_y() == anty:
                                                ant.get_food()

                                        #check if holding food and increase pheromone level
                                        if ant.has_food():
                                                #self.map[ant.get_x()][ant.get_y()].increase_pheromone(PLVL_ADD)
                                                #check if at home with food, drop food, increase pheromone of trip
                                                if self.home.get_x() == antx and self.home.get_y() == anty:
                                                        return_trip = ant.get_tour()
                                                        #calculate amount of pheromone to drop
                                                        print "trail length: " + str(len(return_trip))
                                                        pdrop = float(float(PLVL_ADD)/float(len(return_trip)*len(return_trip)))
                                                        print str(pdrop)

                                                        #for each move in return trip, increase pheromone
                                                        for move in return_trip:
                                                                self.map[move.get_x()][move.get_y()].increase_pheromone(pdrop)
                                                        ant.drop_food()
                                                        self.stockpile = self.stockpile + 1
                                                        
                                        
                                        
			
                	#increment iteration
			self.n_iterations = self.n_iterations + 1

                        #every 10 iterations, increase, decrease or leave alone pheromone drop level
                        if self.n_iterations % 50 == 0:
                                homex = self.home.get_x()
                                homey = self.home.get_y()
                                pincrease = 0             #-1: decrease, 0: don't change, 1: increase

                                #check if need to change plvl drop based on spaces around home
                                #left of home
                                if homex - 1 >= 0 and pincrease != -1:
                                        plvl = self.map[homex - 1][homey].get_pheromone()
                                        if plvl < 5:
                                                pincrease = 1
                                        elif plvl > 25:
                                                pincrease = -1
                                #right of home
                                if homex + 1 < MAP_WIDTH and pincrease != -1:
                                        plvl = self.map[homex + 1][homey].get_pheromone()
                                        if plvl < 5 and pincrease != -1:
                                                pincrease = 1
                                        elif plvl > 25:
                                                pincrease = -1
                                #top of home
                                if homey - 1 >= 0 and pincrease != -1:
                                        plvl = self.map[homex][homey - 1].get_pheromone()
                                        if plvl < 5 and pincrease != -1:
                                                pincrease = 1
                                        elif plvl > 25:
                                                pincrease = -1
                                #bottom of home
                                if homey + 1 >= 0 and pincrease != -1:
                                        plvl = self.map[homex][homey + 1].get_pheromone()
                                        if plvl < 5 and pincrease != -1:
                                                pincrease = 1
                                        elif plvl > 25:
                                                pincrease = -1
                                global PLVL_ADD
                                if pincrease == -1 and PLVL_ADD > 0:
                                        PLVL_ADD = PLVL_ADD - 1
                                elif pincrease == 1:
                                        PLVL_ADD = PLVL_ADD + 1
                                
		self.labeltop.config(text="Iteration: " + str(self.n_iterations) + "   Ants: " + str(len(self.ant_list)) + "   Food collected: " + str(self.stockpile))
		self.label_padd.config(text=str(PLVL_ADD) + "/trip^2")
                        
		self.draw_map()		#redraw map
                self.root.after(self.delay, self.update)






###################   "MAIN"   ###############
app = ACOworld_tk()
app.mainloop()









