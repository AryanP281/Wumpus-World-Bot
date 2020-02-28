#*******************************Imports********************************
from flask import render_template, url_for, redirect, request
from wumpusWorld import app
from wumpusWorld.room import Vector2D, RoomConditions, RoomTypes, are_valid_coords
from wumpusWorld.cave import Cave
from wumpusWorld.bot import Bot

#*******************************Global Variables********************************
cave_dims = Vector2D(4,4) #The dimensions of the cave grid
cave_grid =  [] #The cave grid
cave = Cave(cave_dims) #An instance of the cave object representing the cave
bot = Bot(cave_dims, Vector2D(0,0), cave) #The bot which will play the game
bot_path = bot.traverse_cave()

game_end = 0 #The manner in which the game ended
if(cave.grid[bot_path[-1].x][bot_path[-1].y].room_type == RoomTypes.Pit) :
    game_end = 1
elif(cave.grid[bot_path[-1].x][bot_path[-1].y].room_type == RoomTypes.Wumpus) :
    game_end = 2

player_path = [(0,0)]

bot_last_move = 0 #The index of the last displayed move in the bots path

#*******************************Routing Functions********************************
@app.route("/")
def main() :
    """Initializes the app"""

    #Initializing the cave grid
    initialize_cave()

    return redirect(f"/gamescreen")

@app.route("/gamescreen", methods=["GET", "POST"])
def game_screen() :
    """The game window"""
    #Getting the next move made by the bot
    get_and_display_bots_next_move()

    return render_template("game_screen.html",cave=cave_grid, room_conditions=get_room_conditions(bot_path[bot_last_move]), game_end=game_end, paths_traversed=bot.paths_traversed)

@app.route("/map")
def display_map() :
    """Displays the game map"""

    #Generating the map gui
    cave_map = get_cave_map()

    return render_template("game_map.html", map=cave_map)

@app.route("/play", methods=["GET", "POST"])
def play_game() :
    """Allows the player to play the game"""
    if(request.method == "GET") :   
        return render_template("play_game.html", rows=cave_dims.x, cols=cave_dims.y, player_path=player_path, room_conditions=get_room_conditions(player_path[-1]))
    else :
        btn = list(request.form.keys())[0] #The name of the button that was pressed
        if(btn == "up") :
            new_pos = Vector2D(player_path[-1][0], player_path[-1][1]) + Vector2D(-1,0)
            if(are_valid_coords(new_pos, cave_dims)) :
                player_path.append(new_pos.to_tuple())
        if(btn == "down") :
            new_pos = Vector2D(player_path[-1][0], player_path[-1][1]) + Vector2D(1,0)
            if(are_valid_coords(new_pos, cave_dims)) :
                player_path.append(new_pos.to_tuple())
        if(btn == "left") :
            new_pos = Vector2D(player_path[-1][0], player_path[-1][1]) + Vector2D(0,-1)
            if(are_valid_coords(new_pos, cave_dims)) :
                player_path.append(new_pos.to_tuple())
        if(btn == "right") :
            new_pos = Vector2D(player_path[-1][0], player_path[-1][1]) + Vector2D(0,1)
            if(are_valid_coords(new_pos, cave_dims)) :
                player_path.append(new_pos.to_tuple())

        return render_template("play_game.html", rows=cave_dims.x, cols=cave_dims.y, player_path=player_path, room_conditions=get_room_conditions(player_path[-1]))


@app.route("/debug")
def debug() :
    """A page used for debugging purposes"""

    return "Debug"

#*******************************Helper Functions********************************
def initialize_cave() :
    """Initializes the cave grid GUI"""

    #Loading global variables
    global cave_grid
    cave_grid = []

    #Initializing the cave grid GUI
    for row in range(0, cave_dims.x) :
        cave_grid.append([]) #Adding a row to the grid
        for col in range(0, cave_dims.y) :
            cave_grid[row].append(0) 

def get_room_conditions(room_coords) :
    """Returns the conditions in the given room in string form"""
    
    #Checking if the bot has reached the gold
    if(cave.grid[bot_path[bot_last_move].x][bot_path[bot_last_move].y].room_type == RoomTypes.Gold) :
        return ["Gold"]
    #Checking if the bot fell into a pit
    elif (cave.grid[bot_path[bot_last_move].x][bot_path[bot_last_move].y].room_type == RoomTypes.Pit) :
        return ["Pit"]
    #Checking if the bot was killed by the Wumpus
    elif(cave.grid[bot_path[bot_last_move].x][bot_path[bot_last_move].y].room_type == RoomTypes.Wumpus) :
        return ["Wumpus"]
    else :
        #Getting the conditions in the room
        if(type(room_coords) == tuple) :
            conditions = cave.grid[room_coords[0]][room_coords[1]].get_conditions()
        else :
            conditions = cave.grid[room_coords.x][room_coords.y].get_conditions()

        #Converting the conditions to string
        str_conditions = []
        if(len(conditions) == 0) :
            str_conditions.append("Empty")
        else :
            for condition in conditions :
                if(condition == RoomConditions.Breeze) :
                    str_conditions.append("Breeze")
                elif (condition == RoomConditions.Stench) :
                    str_conditions.append("Stench")

        return str_conditions

def get_and_display_bots_next_move() :
    """Gets the bot next move and displays it on the screen"""

    #Loading global variables
    global cave_grid, bot_last_move, bot_path

    #Checking the entire path has been displayed
    if(bot_last_move != len(bot_path) - 1) :
        cave_grid[bot_path[bot_last_move].x][bot_path[bot_last_move].y] = 1 #Displaying the last travelled room as empty
        bot_last_move += 1 #Updating the last move counter
        cave_grid[bot_path[bot_last_move].x][bot_path[bot_last_move].y] = 2

def get_cave_map() :
    """Gets and encodes the cave map data"""

    #Loading the global variables
    global cave

    map_data = [] #The buffer which holds the map data

    for row in cave.grid :
        map_data.append([]) #Adding a row
        for room in row :
            if(room.room_type == RoomTypes.Empty or room.room_type == RoomTypes.Start) :
                map_data[-1].append(0)
            elif (room.room_type == RoomTypes.Pit) :
                map_data[-1].append(1)
            elif (room.room_type == RoomTypes.Wumpus) :
                map_data[-1].append(2)
            elif(room.room_type == RoomTypes.Gold) :
                map_data[-1].append(3)
    
    return map_data

