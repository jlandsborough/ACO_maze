

class Location:
	#constructor
	def __init__(self):
		self.pos_x = 0
		self.pos_y = 0
		self.food_source = 0
		self.home = 0
		self.blocked = 0
		self.pheromone_level = 0

	#set location to x and y
	def set_location(self, x, y):
		self.pos_x = x
		self.pos_y = y
	
	#set location as a food source
	def set_food_source(self):
		self.food_source = 1

	#unset location as a food source
	def unset_food_source(self):
		self.food_source = 0

	#determine if location is a food source
	def is_food_source(self):
                if self.food_source == 1:
                        return 1
                else:
                        return 0

	#set location as colony home
	def set_home(self):
		self.home = 1

	#unset location as colony home
	def unset_home(self):
		self.home = 0

        #determine if location is set as home
	def is_home(self):
                if self.home == 1:
                        return 1
                else:
                        return 0

	#determine if location is blocked
	def is_blocked(self):
		if self.blocked == 1:
			return 1
		else:
			return 0

	#set location as blocked (by a wall)
	def set_blocked(self):
		self.blocked = 1

	#unset location as blocked (by a wall)
	def unset_blocked(self):
		self.blocked = 0

        #get x-value of location
        def get_x(self):
                return self.pos_x

        #get y-value of location
        def get_y(self):
                return self.pos_y

        #increases the pheromone level for location
        def increase_pheromone(self, level):
                self.pheromone_level = self.pheromone_level + level

        #decreases the pheromone level for location
        def decrease_pheromone(self, level):
                #self.pheromone_level = float(self.pheromone_level * 0.9)
                self.pheromone_level = self.pheromone_level - level
                if self.pheromone_level < .1:
                        self.pheromone_level = 0

        #get pheromone level for location
        def get_pheromone(self):
                return self.pheromone_level
