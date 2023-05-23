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
c.execute("CREATE TABLE IF NOT EXISTS lyrics(name TEXT, lyr TEXT, UNIQUE(name, lyr))")


songs = [f for f in listdir('./lyrics/STORAGE') if isfile(join('./lyrics/STORAGE', f))]
connections = []

for i in range(len(songs)):
    file = open("./lyrics/STORAGE/" + songs[i], "r")
    lyrics = file.read()

    # lyrics = lyrics.replace(",", "") # For json reasons?
    lyrics = lyrics.replace("(", "")
    lyrics = lyrics.replace(")", "")
    lyrics = lyrics.replace("\"", "")
    lyrics = lyrics.replace("“", "")
    lyrics = lyrics.replace("”", "")
    lyrics = re.sub(r'_+(.*\n*)*', "", lyrics) #metadata handling


    try:
        c.execute("INSERT INTO lyrics VALUES (?,?)", (songs[i], lyrics))
        db.commit()
    except:
        pass


    lyrics = lyrics.split()

    for keylen in range(1,11):
        connections += [{}]
        for j in range(len(lyrics) - keylen): # Do for key length up to 10
            word = lyrics[j:j+keylen]
            word = " ".join(word)
            nextWords = connections[keylen-1].get(word, [])
            if(len(nextWords) > 0):
                nextWords += [lyrics[j+keylen]]
            else:
                connections[keylen-1].update({word: [lyrics[j+keylen]]})

db.close()

for i in range(1,11):
    out = open("./lyrics/data" + str(i) + ".txt", "w")
    json.dump(connections[i-1], out)
    # out.write(str(connections))
    out.close()


##################
### PART THREE ###
##################
import json

data = open("./lyrics/data10.txt", "r")
data = json.load(data)
print(data)


# temp = list(c.execute("SELECT name FROM lyrics").fetchall())
# print(len(temp))
# db.close()
