#*******************************Imports*******************************
from enum import Enum
import copy

#*******************************Enums********************************
class RoomTypes(Enum) :
    Empty = 0
    Pit = 1
    Wumpus = 2
    Gold = 3 
    Start = 4

class RoomConditions(Enum) :
    Breeze = 0
    Stench = 1

#*******************************Functions********************************
def are_valid_coords(coords, grid_dims) :
    """Checks if the given coordinates tuple is valid"""

    if(coords.x >= 0 and coords.y >= 0) :
        if(coords.x < grid_dims.x and coords.y < grid_dims.y) :
            return True
    
    return False

def get_coords(rooms) :
    """Returns the Vector2D coordinates of the rooms in the given list"""

    coords = []
    for room in rooms :
        coords.append(room.coords)

    return coords

#*******************************Classes********************************
class Vector2D(object) :
    def __init__(self, x=0, y=0) :
        self.X(x)
        self.Y(y)
    
    def X(self, x) :
        """Sets the x value of the vector""" 

        self.x = x

    def Y(self,y) :
        """Sets the y value of the vector"""

        self.y = y

    def __repr__(self) :
        """Returns a printable version of the vector"""

        return str([self.x, self.y])

    def __eq__(self, other) :
        """Checks if the 2 vectors are equal"""

        if(self.x == other.x and self.y == other.y) :
            return True
        return False

    def __ne__(self, other) :
        return not self.__eq__(other)

    def __add__(self,other) :
        """Adds the 2 vectors"""

        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other) :
        """Subtracts the 2 vectors"""

        return Vector2D(self.x - other.x, self.y - other.y)

    def to_tuple(self) :
        """Returns a tuple representation of itself"""

        return (self.x, self.y)

class Room(object) :

    neighbour_pos_vectors = (Vector2D(-1,0), Vector2D(0, 1), Vector2D(0, -1), Vector2D(1,0)) #Vectors to the positions of neighbours..
    #...from the current room's position
    
    def __init__(self, coords, room_type=RoomTypes.Empty, room_conditions=[]) :
        """coords=Vector2D object containing the coordinates of the room in the network.
        grid_dims=tuple containing the dimensions of the room grid
        room_type=type of room i.e RoomTypes.Normal, RoomTypes.Pit, RoomTypes.Wumpus or RoomTypes.Gold
        room_conditions=inputs received by the bot on entering the room i.e RoomConditions.Breeze or RoomConditions.Stench"""

        #Setting room properties
        self.coords = coords #The coordinates of the room in the grid
        self.room_type = room_type #The room type
        self.room_conditions = copy.copy(room_conditions) #The room conditions
        self.neighbours = [] #The room's neighbour rooms

    def set_room_coordinates(self, new_coords) :
        """Changes the coordinates of the room"""
        self.coords = new_coords

    def set_room_type(self, room_type) :
        """Sets the type of room to the given type.
        room_type=type of room i.e RoomTypes.Normal, RoomTypes.Pit, RoomTypes.Wumpus or RoomTypes.Gold"""
 
        self.room_type = room_type

        #Updating the neighbours
        self.update_neighbour_conditions()

    def set_room_conditions(self, room_conditions) :
        """Sets the type of room to the given type.
        room_conditions=inputs received by the bot on entering the room i.e RoomConditions.Breeze or RoomConditions.Stench"""

        self.room_conditions = room_conditions

    def set_neighbours(self, neighbours) :
        """Sets the neighbours to the current room"""

        self.neighbours = copy.copy(neighbours)

    def get_conditions(self) :
        """"Returns the conditions in the room"""

        conditions = [] #The conditions in the room
        for condition in self.room_conditions :
            if(not condition[1] in conditions) :
                conditions.append(condition[1])

        return conditions

    def update_neighbour_conditions(self) :
        """Updates the conditions in the neighbouring rooms according to the type of the current room"""

        #Checking if the room contains a pit
        if(self.room_type == RoomTypes.Pit) :
            #Setting neighbours' conditions to breezy
            for neighbour in self.neighbours :
                if(not (n := (self.coords, RoomConditions.Breeze)) in neighbour.room_conditions) :
                    neighbour.room_conditions.append(n)

        #Checking if the room contains Wumpus
        if(self.room_type == RoomTypes.Wumpus) :
            #Setting neighbours' conditions to Stench
            for neighbour in self.neighbours :
                if(not (n := (self.coords, RoomConditions.Stench)) in neighbour.room_conditions) :
                    neighbour.room_conditions.append(n)

        #Checking if room is empty
        if(self.room_type == RoomTypes.Empty) :
            for neighbour in self.neighbours :
                #Removing any effects on the neighbours
                for effect in neighbour.room_conditions :
                    if(effect[0] == self.coords) :
                        neighbour.room_conditions.remove(effect)

        #Checking if the room is the starting room
        if(self.room_type == RoomTypes.Start) :
            #Setting all the neighbours to empty
            for neighbour in self.neighbours :
                #Checking if the room can be moved to from the current pos
                if((neighbour.coords - self.coords) in self.neighbour_pos_vectors[:4]) :
                    neighbour.set_room_type(RoomTypes.Empty)

    def __eq__(self, other) :
        return self.coords == other.coords