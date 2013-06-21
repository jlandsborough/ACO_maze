from Location import Location
import random

class Ant:

        #constructor
	def __init__(self, x, y):
		self.food = 0
		self.pos_x = x
		self.pos_y = y
		self.prev_x = x
		self.prev_y = y
		self.history = []
		

        #determine if ant has food
	def has_food(self):
		if self.food == 1:
			return 1
		else:
			return 0

        #set ant to hold food
	def get_food(self):
		self.food = 1
		self.prev_x = self.pos_x
		self.prev_y = self.pos_y

        #set ant to drop food
	def drop_food(self):
		self.food = 0
		self.prev_x = self.pos_x
		self.prev_y = self.pos_y
		del self.history[:] #delete return trip
		
	
	#get x coordinate of ant location
        def get_x(self):
                return self.pos_x

        #get y coordinate of ant location
        def get_y(self):
                return self.pos_y

        #get previous x coordinate (to avoid moving backwards)
        def get_prev_x(self):
                return self.prev_x

        #get previous y coordinate (to avoid moving backwards)
        def get_prev_y(self):
                return self.prev_y

        #get list of moves made during return trip
        def get_tour(self):
                return self.history

        def move_attractiveness(self, move):
                if move in self.history:
                        print "SEEN BEFORE!!!!"
                        return 0.1
                else:
                        return 1

        #move ant to new location
        def move(self, movelist):
                # previous move is current location
                self.prev_x = self.pos_x
                self.prev_y = self.pos_y
                
                alpha = 1       #pheromone influence
                beta = 1        #desirability influence
                sum = 0
                i = 0
                totalp = 0 #running total of pheromone
                rand_num = int(random.random() * 100) #random number between 0 and 100
                #print "Rand: " + str(rand_num)
                #get sum of pheromone levels
                for move in movelist:
                        #if not carrying food, and move is food source, move there
                        if not self.food and move.is_food_source():
                                self.pos_x = move.get_x()
                                self.pos_y = move.get_y()
                                return
                        #if carrying food and move is home, move there
                        if self.food and move.is_home():       
                                self.pos_x = move.get_x()
                                self.pos_y = move.get_y()
                                return
                        d = 1
                        #calculate desirability
                        if move in self.history:
                                #print "SEEN BEFORE!!!" + str(pow(0.1, 1))
                                d = 0.1
                        sum = sum + pow(move.get_pheromone() + 0.1, alpha) * pow(d, beta)
                        
                #        print "Sum: " + str(sum)
                for move in movelist:
                        d = 1
                        #calculate desirability
                        if move in self.history:
                                #print "SEEN BEFORE!!!" + str(pow(0.1, 1))
                                d = 0.1 #discourages looping
                        i = i + 1
                        totalp = totalp + float(float(pow(move.get_pheromone() + 0.1, alpha) * pow(d, beta))/float(sum))*100
                #        print "totalp: " + str(totalp)
                        #if random number is <= totalpercentage, choose that move
                        if rand_num <= totalp:
                               self.pos_x = move.get_x()
                               self.pos_y = move.get_y()
                               if self.food and move not in self.history:
                                       self.history.append(move)
							
							   
                               return
