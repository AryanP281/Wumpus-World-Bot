#**********************************Imports******************************
import copy
import random
from wumpusWorld.room import Vector2D, RoomTypes, get_coords, RoomConditions
from wumpusWorld.cave import Cave
from wumpusWorld.misc import get_num_of_occurrences, intersection

#**********************************Classes******************************
class Bot(object) :
    def __init__(self, grid_dims, start_pos, cave) :

        #Initializing the bot's world view
        self.world_view = [] #A 2d array containing the rooms as perceived by the bot
        self.cave = cave
        self.initialize_world_view(start_pos)

        #Initializing the closed and open lists
        self.closed_list = [start_pos]
        self.open_list = []

        #Initializing the bot's attributes
        self.paths_traversed = 0 #The paths traversed in the last cave (before dying or reaching gold)

    def initialize_world_view(self, start_pos) :
        """Initializes the bot's world view to empty rooms"""

        #Looping through the grid rows
        for row in range(0, self.cave.dims.x) :
            self.world_view.append([]) #Adding a new row
            #Looping through the grid columns
            for col in range(0, self.cave.dims.y) :
                if(row == start_pos.x and col == start_pos.y) :
                    self.world_view[row].append([[], -1])
                else :
                    self.world_view[row].append([[], 0])

    def traverse_cave(self) :
        """Traverses the cave to reach the gold"""

        #Initializing the paths
        current_path = [self.closed_list[-1]] #The path currently traversed
        paths = [current_path] #A list of all the traversed

        #Getting the path
        path = self.traverse_path(paths, current_path)

        return path

    def traverse_path(self, paths, current_path) :
        """Traverses the given path"""

        #Checking if the room contains
        current_room_type = self.cave.grid[current_path[-1].x][current_path[-1].y].room_type #The type of the current room
        neighbours = get_coords(self.cave.grid[current_path[-1].x][current_path[-1].y].neighbours) #The neighbours of the current room
        #Checking if the bot found the gold
        if(current_room_type == RoomTypes.Gold ) :
            print("Found Gold")
            self.paths_traversed = len(paths)
            return current_path
        #Checking if the bot is dead
        elif(current_room_type == RoomTypes.Pit or current_room_type == RoomTypes.Wumpus) :
            print("Dead")
            self.paths_traversed = len(paths)
            return current_path
        #Marking the room as safe
        else :
            #Checking if it was already know that the room is safe
            if(self.world_view[current_path[-1].x][current_path[-1].y][1] != -1) :
                #Updating the world view of the neighbours, now that it is known that room is safe
                for neighbour in neighbours :
                    if(not self.world_view[neighbour.x][neighbour.y][1] in (-1,0,1) and len(intersection(self.world_view[neighbour.x][neighbour.y][0],neighbours))) :
                        self.update_room_view(neighbour)
                self.world_view[current_path[-1].x][current_path[-1].y] = [[None, -1], -1]

        #Updating the world view of neighbours
        self.update_view_of_neighbours(current_path[-1])

        #Adding the neighbours of the current room to the open list
        for neighbour in neighbours :
            if(not neighbour in self.open_list and not neighbour in self.closed_list) :
                self.open_list.append(neighbour)

        #Getting the next room to move to
        next_room = self.get_next_move(neighbours)

        #Updating the open and closed lists
        self.open_list.remove(next_room)
        self.closed_list.append(next_room)

        #Checking if the path has branched
        if(not next_room in neighbours) :
            new_path = self.manage_paths(paths, next_room) #Creating a new path-branch
            paths.append(new_path) #Adding the new path to the list of paths
            return self.traverse_path(paths, new_path) #Traversing the new path
        else :
            current_path.append(next_room)
            return self.traverse_path(paths, current_path)

    def update_view_of_neighbours(self, room) :
        """Updates the bot's view of the neighbouring rooms based on the conditions in the given room"""

        #Checking if the view of the neighbours has already been altered by this room
        if(get_num_of_occurrences(self.closed_list, room) == 1) :
            #Getting the neighbours' coords
            neighbours = get_coords(self.cave.grid[room.x][room.y].neighbours)

            #Getting the room conditions
            room_conditions = self.cave.grid[room.x][room.y].get_conditions()

            #Checking if the room is breezey
            if(RoomConditions.Breeze in room_conditions or RoomConditions.Stench in room_conditions) :
                #Updating the view of the neighbours
                for neighbour in neighbours :
                    danger_prob = self.world_view[neighbour.x][neighbour.y][1] #The probability that the neighbour contains danger
                    #Checking if it has already been determined that the neighbour doesn't contain danger
                    if(danger_prob != -1) :
                        new_danger_probability = 1.0 / self.get_sample_space_size(room) #The increment in danger probability
                        self.world_view[neighbour.x][neighbour.y][1] = max(1, danger_prob + new_danger_probability)
                        self.world_view[neighbour.x][neighbour.y][0].append(room)
            else :
                #Updating the view of the neighbours
                for neighbour in neighbours :
                    #Checking if the room was earlier believed to be dangerous
                    if(not self.world_view[neighbour.x][neighbour.y][1] in (-1,0,1)) :
                        self.update_room_view(neighbour)
                    #Updating the view of the neighbour
                    self.world_view[neighbour.x][neighbour.y][1] = -1 


    def get_sample_space_size(self, room) :
        """Gets the no. of dangerous neighbours of the room i.e no. of neighbours with danger_prob != -1"""

        neighbours = get_coords(self.cave.grid[room.x][room.y].neighbours)
        sample_space_size = 0

        for neighbour in neighbours :
            if(self.world_view[neighbour.x][neighbour.y][1] != -1) :
                sample_space_size += 1

        return sample_space_size

    def update_room_view(self, room) :
        """Updates the bots view of the room"""

        for neighbour_room in self.world_view[room.x][room.y][0] :
            #Finding the other rooms in opne_list marked unsafe by neighbour_room
            for a in self.open_list :
                #Checking if the room was already determined to be safe and if it is a affected neighbour of neighbour_room
                if(not self.world_view[a.x][a.y][1] in (-1,0,1) and a in get_coords(self.cave.grid[neighbour_room.x][neighbour_room.y].neighbours)) :
                    #Increasing the probability that the room is dangerous, as the sample space has decreased by 1 point
                    self.world_view[a.x][a.y][1] += ((self.get_sample_space_size(neighbour_room) - 1)**-1) - (self.get_sample_space_size(neighbour_room)**-1)


    def get_next_move(self, neighbours) :
        """Selects and returns the next moves from the open_list"""

        next_moves = [self.open_list[0]]
        min_prob = self.world_view[self.open_list[0].x][self.open_list[0].y][1]
        for a in range(1, len(self.open_list)) :
            room_prob = self.world_view[self.open_list[a].x][self.open_list[a].y][1]
            if(room_prob < min_prob) :
                next_moves.clear()
                next_moves.append(self.open_list[a])
                min_prob = room_prob
            elif (room_prob == min_prob) :
                next_moves.append(self.open_list[a])

        if(len(next_moves) > 1) :
            for next_move in next_moves :
                if(next_move in neighbours) :
                    return next_move
            return next_moves[random.randrange(0, len(next_moves))]
        elif(len(next_moves) == 1) :
            return next_moves[0]
        elif(len(next_moves) == 0) :
            raise Exception("No traversable room found")

    def manage_paths(self, paths, room) :
        """Creates a new path in case of branching"""

        neighbours = get_coords(self.cave.grid[room.x][room.y].neighbours) #The neighbours of the given room

        path_found = False #Indicates whether the path to which the node belongs has been found
        new_paths = [] #The new paths

        #Looping through the neighbours
        for neighbour in neighbours :
            for path in paths :
                #Checking whether the path contains the neighbour
                if(neighbour in path) :
                    new_paths.append(path[:path.index(neighbour) + 1] + [room])

        if(len(new_paths) == 0) :
            raise Exception("No path found")
        
        return self.get_shortest_path(new_paths)

    def get_shortest_path(self, paths) :
        """Returns the shortest path from the list of paths"""

        shortest_path = 0

        for a in range(1, len(paths)) :
            if(len(paths[a]) < len(paths[shortest_path])) :
                shortest_path = a

        return paths[shortest_path]