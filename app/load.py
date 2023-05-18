################
### PART ONE ###
################

# from os import listdir
# from os.path import isfile, join
# import random
# import subprocess
#
# songs = [f for f in listdir('./lyrics') if isfile(join('./lyrics', f))]
# # print(onlyfiles)
#
# # toKeep = []
#
# for i in range(100):
#     x = random.randint(0,len(songs)-1)
#     # toKeep += [songs[x]]
#     songs.pop(x)
#     subprocess.run(["mv", "./lyrics/" + songs[x], "./lyrics/STORAGE"], capture_output=True, text=True)

# -18


################
### PART TWO ###
################

from os import listdir
from os.path import isfile, join
import random
import subprocess
import re
import json


import sqlite3
db = sqlite3.connect("lyrics.db", check_same_thread=False) #CRUCIAL
global c
c = db.cursor()
c.execute("CREATE TABLE if not exists lyrics(name TEXT, lyr TEXT)")


songs = [f for f in listdir('./lyrics/STORAGE') if isfile(join('./lyrics/STORAGE', f))]
connections = {}

for i in range(len(songs)):
    file = open("./lyrics/STORAGE/" + songs[i], "r")
    lyrics = file.read()

    # lyrics = lyrics.replace(",", "") # For json reasons?
    lyrics = lyrics.replace("(", "")
    lyrics = lyrics.replace(")", "")
    lyrics = lyrics.replace("\"", "")
    lyrics = lyrics.replace("“", "")
    lyrics = lyrics.replace("”", "")
    lyrics = re.sub(r'_+(.*\n*)*', "", lyrics)


    c.execute("INSERT INTO lyrics VALUES (?,?)", (songs[i], lyrics))
    db.commit()


    lyrics = lyrics.split()
    for j in range(len(lyrics) - 1): # Do for key length up to 10
        word = lyrics[j]
        nextWords = connections.get(word, [])
        if(len(nextWords) > 0):
            nextWords += [lyrics[j+1]]
        else:
            connections.update({word: [lyrics[j+1]]})

db.close()

out = open("./lyrics/data.txt", "w")
json.dump(connections, out)
# out.write(str(connections))
out.close()


##################
### PART THREE ###
##################
import json

data = open("./lyrics/data.txt", "r")
data = json.load(data)
# print(data)
