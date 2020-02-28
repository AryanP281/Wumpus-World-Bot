#*******************************Imports********************************
import random
from math import ceil
from wumpusWorld.room import Room, RoomTypes, RoomConditions, Vector2D, are_valid_coords

#*******************************Classes********************************
class Cave(object) :

    pit_probability = 0.2 #The probability of a room having a pit
    
    def __init__(self, grid_dims, start_pos=Vector2D(0,0), generate_cave=True) :
        """"grid_dims=Vector2D object containing the dimensions of the cave grid"""

        if(generate_cave) :
            #Setting the cave properties
            self.dims = grid_dims
            self.start_pos = start_pos

            #Creating the cave structure
            self.grid = [] #The cave grid
            self.create_cave_structure()

            self.grid[0][2].set_room_type(RoomTypes.Pit)

            #Styling the cave
            self.design_cave()

            print(f"Cave {id(self)} instantiated")


    def create_cave_structure(self) :
        """Creates the cave structure"""

        #Looping through the rows in the grid
        for row in range(0, self.dims.x) :
            self.grid.append([]) #Adding a row to the grid
            #Looping through the columns
            for col in range(0, self.dims.y) :
                self.grid[row].append(Room(Vector2D(row, col)))

        #Linking the rooms to each other
        self.link_rooms()

    def link_rooms(self) :
        """Links the rooms in the cave"""

        for row in range(0, self.dims.x) :
            for col in range(0, self.dims.y) :
                self.link_room(self.grid[row][col])

    def link_room(self, room) :
        """Finds the neighbours to the given room and links them"""

        neighbours = [] #A list of the neighbours 

        #Looping through the possible position vectors to neighbouring rooms
        for pos_vec in Room.neighbour_pos_vectors :
            neighbour_coords = room.coords + pos_vec #The coordinates of the neighbour according to the position vector
            #Checking if the neighbour is valid
            if(are_valid_coords(neighbour_coords, self.dims)) :
                neighbours.append(self.grid[neighbour_coords.x][neighbour_coords.y])

        #Updating the room's neighbours list
        room.set_neighbours(neighbours)

    def design_cave(self) :
        """Designs the cave by setting the room types"""
        
        #Setting the starting room
        self.grid[self.start_pos.x][self.start_pos.y].set_room_type(RoomTypes.Start)

        #Placing the gold 
        gold_room_x = random.randrange(ceil(len(self.grid) / 2), len(self.grid))
        gold_room_y = random.randrange(ceil(len(self.grid[0]) / 2), len(self.grid[0]))
        self.grid[gold_room_x][gold_room_y].set_room_type(RoomTypes.Gold)

        #Placing the Wumpus
        self.place_wumpus()

        #Placing the pits
        self.place_pits()


    def place_wumpus(self) :
        """Chooses a room to place the Wumpus"""

        #Looping till a room is found for the wumpus
        while(True) :
            #Randomly selecting a room
            wumpus_room = self.grid[random.randrange(0, self.dims.x)][random.randrange(0, self.dims.y)]

            #Ensuring that the room is not the starting room or the gold room and is not a neighbour of the starting room
            if(wumpus_room.room_type != RoomTypes.Start and not wumpus_room in self.grid[self.start_pos.x][self.start_pos.y].neighbours and wumpus_room.room_type != RoomTypes.Gold) :
                wumpus_room.set_room_type(RoomTypes.Wumpus) #Placing the wumpus
                break

    def place_pits(self) :
        """Chooses the rooms to place pits"""

        #Looping through the cave grid
        for row in self.grid :
            for room in row :
                rand = random.randrange(1,11,1)
                if(rand <= self.pit_probability * 10) :
                    #Ensuring that the room is not the starting room and is not a neighbour of the starting room
                    if(room.room_type != RoomTypes.Start and not room in self.grid[self.start_pos.x][self.start_pos.y].neighbours) :
                        #Ensuring that the room doesnt already contain the wumpus or the gold
                        if(room.room_type != RoomTypes.Wumpus and room.room_type != RoomTypes.Gold) :
                            room.set_room_type(RoomTypes.Pit) #Placing the pit

