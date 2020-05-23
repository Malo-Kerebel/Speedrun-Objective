import math
import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 0

def get_str_time(run):

    return str(math.floor(run["run"].times['primary_t'] // 60)) + 'm ' + str(math.floor(run["run"].times['primary_t'] % 60)) + 's ' + str(math.floor((run["run"].times['primary_t'] - math.floor(run["run"].times['primary_t']))*1000)+ 1 ) + 'ms'
#I added the + 1 because python get the substraction wrong due to floating point imprecision

name = input("Type the name of your game\n")

print("This are the possible game select the correct one :\n")
for i in range(len(api.search(srcomapi.datatypes.Game, {"name": name}))):
	print (str(i+1) + ") " + str(api.search(srcomapi.datatypes.Game, {"name": name})[i]) + "\n")
game = api.search(srcomapi.datatypes.Game, {"name": name})[int(input())-1]
#All the game that corespond to the query ask before get listed get listed


print("Select the category :\n")
for i in range(len(game.categories)):
	print (str(i+1) + ") " + str(game.categories[i]) + "\n")
category = game.categories[int(input())-1]
#All the categories available for the game selected are listed (for single level it shouldn't work, for exemple the forsaken city of celeste shouldn't be selectable)

game_runs = {}

if not category.name in game_runs:
  game_runs[category.name] = {}
if category.type == 'per-level':
  for level in game.levels:
    game_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
else:
  game_runs[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))
#This get all the runs of the selected category

runs = game_runs[category.name].runs
#All the runs get stored in the list runs

choice = 0

print("Do you aim :\n1) a place\n2) a percentage\n3) a player (experimental and slow feature)\n")
while (choice != 1 and choice != 2 and choice != 3): 
    choice = int(input())

if (choice == 1):
    print ("you need to get below " + get_str_time(runs[int(input("Input the place you aim out of " + str(len(runs)) + " runs :\n"))]))
elif(choice == 2):    
    print ("you need to get below " + get_str_time(runs[math.floor(0.01*len(runs)*int(input("Input the percentage you aim to get :\n")))]))
elif(choice == 3):
    player = input("Input which player time you aim\n")
    current = ""
    i = 0
    print (runs[205]["run"].players[0].name)
    print (runs[206]["run"].players[0].name)
    print (runs[207]["run"].players[0].name)
    print (runs[208]["run"].players[0].name)
    while (player != current and i < len(runs) ):
        current = runs[i]["run"].players[0].name
        i += 1
    
    if (player == current):
        print("you need to get below " + get_str_time(runs[i-1]))
    else:
        print ("The player you named wasn't found")

