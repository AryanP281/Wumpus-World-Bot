from wumpusWorld.cave import Cave
from wumpusWorld.room import Vector2D, RoomTypes
from wumpusWorld.bot import Bot

avg_acc = 0
for epoch in range(0, 20) :
    matches_won = 0
    for a in range(0,100) :
        cave = Cave(Vector2D(4,4))
        bot = Bot(Vector2D(4,4), Vector2D(0,0), cave)
        path = bot.traverse_cave()

        if(cave.grid[path[-1].x][path[-1].y].room_type == RoomTypes.Gold) :
            matches_won += 1

    print(f"Accuracy = {matches_won} %")
    avg_acc += matches_won

print("Avg win rate = {}".format(avg_acc / 20))