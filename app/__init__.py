from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from spotify_api import *
import random

app = Flask(__name__)
app.secret_key = os.urandom(32) # This is NOT secure

# For lyric generation
lines = 30
similarity = 1
song1 = ""
song2 = ""

@app.route("/", methods=['GET', 'POST'])
def log_in():
    global lines, similarity, song1, song2
    lines = 30
    similarity = 1
    song1 = ""
    song2 = ""
    if 'username' in session: # If already logged in
        return render_template('home.html', user = session["username"])
    return render_template('login.html') # For login AND signup

@app.route('/logout')
def logout():
    if (session):
        session.pop('username')
    return redirect('/')

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        return render_template('home.html', user = session['username'])

@app.route("/login", methods=['GET','POST'])
def authenticate():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form['username']
    pw = request.form['password']
    if login(user,pw):
        session['username'] = request.form['username']
        return render_template('home.html', user = session['username'])
    else:
        return render_template('login.html', errorTextL = "Authentication Failed")
    return redirect('/')

@app.route('/signup', methods = ["POST"])
def sign_up():
    if 'username' in session:
        return redirect("/")
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if signup(user,pw):
            return render_template('login.html', successText = "Sign up successful")
        else:
            return render_template('login.html', errorTextS= "User already exist")
    else:
        return render_template('login.html', errorTextS = "User already exist")

@app.route('/profile', methods = ['POST','GET'])
def profile():
    if request.method == 'POST':
        return render_template('profile.html', Username = session['username'])

@app.route('/change_pw', methods = ['GET','POST'])
def changepw():
    if request.method == 'GET':
        old = request.args['oldpass']
        new = request.args['newpass']
        confirm = request.args['confirmpass']
        if(old != select_from("user.db", "users", "password", session['username'], "username")):
            return render_template('profile.html', message = "Authentication fail, wrong password entered", Username = session['username'])
        if (new != confirm):
            return render_template('profile.html', message = "Password Don't match",Username = session['username'])
        message = DB_changepw(session['username'], new)
        return render_template('profile.html', message = message, Username = session['username'])
    return render_template('profile.html')
@app.route('/artist', methods = ["POST"])
def toArtist():
    if request.method == 'POST':
        return render_template('artist.html')

@app.route('/artists', methods = ['GET', 'POST'])
def artist():
    if request.method == 'POST':
        if not request.form['artist_name']:
            return render_template('artist.html', message = "Input is empty")
        else:
            artist = request.form['artist_name']
            token = get_token()
            result = search_for_artist(token, artist)
            artist_id = result["id"]
            songs = get_songs_by_artist(token, artist_id)
            return render_template('artist.html', data = songs, artist = "Top 10 Songs by " + artist)
    else:
        return render_template('artist.html')

@app.route('/lyrics', methods = ['GET','POST'])
def lyrics(newtext="", mixtext=""):
    if 'username' in session:
        if (len(newtext) == 0): #weird handling?
            newtext = ""
        else:
            pass

        db = sqlite3.connect("lyrics.db", check_same_thread=False) #CRUCIAL
        global c
        c = db.cursor()
        temp = list(c.execute("SELECT name FROM lyrics").fetchall())
        allSongs = []
        for element in temp:
            allSongs += [element[0]]
        # print(allSongs)
        db.close()

    return render_template('lyrics.html', newText = newtext, dLines = lines, dSim = similarity, songlist = allSongs, input1=song1, input2=song2, mixText=mixtext)

@app.route('/generate', methods = ['POST'])
def generate():
    data = open("./lyrics/data" + str(similarity) + ".txt", "r")
    data = json.load(data)

    text = request.form.to_dict(flat=False)["line"][0]
    words = list(data.keys())
    try:
        nextWords = data.get(" ".join(text.split()[len(text.split())-similarity:])) #use .get instead of []. [] errors on bad key, .get returns None and allows for edit distance
        print("trying...")
    except:
        print("NOPE")
        return redirect('/lyrics')

    if (nextWords == None):
        nextWords = data[words[random.randint(0,len(words))]]

    if (not (len(text) == 0) and not (text[len(text)-1] == " ")):
        text += " "

    wordsOnLine = 0
    for i in range(lines * 6): #words per line
        newWord = nextWords[random.randint(0, len(nextWords)-1)]
        try:
            nextWords = data[newWord]
        except:
            nextWords = data[words[random.randint(0,len(words))]]
        text += newWord + " "
        wordsOnLine += 1
        if (wordsOnLine == 6):
            text += "<br>"
            wordsOnLine = 0

    return lyrics(newtext=text) #weird?

@app.route('/song1', methods = ['GET', 'POST'])
def songSelect1():
    if 'username' in session: # If already logged in
        global song1
        song1 = request.args.to_dict(flat=False)['songs1'][0]
        return redirect('/lyrics')
    return render_template('home.html')

@app.route('/song2', methods = ['GET', 'POST'])
def songSelect2():
    if 'username' in session: # If already logged in
        global song2
        song2 = request.args.to_dict(flat=False)['songs2'][0]
        return redirect('/lyrics')
    return render_template('home.html')

@app.route('/mix', methods = ['GET', 'POST'])
def mix():
    if 'username' in session: # If already logged in
        db = sqlite3.connect("lyrics.db", check_same_thread=False) #CRUCIAL
        global c
        c = db.cursor()

        try:
            lyrics1 = list(c.execute("SELECT lyr FROM lyrics WHERE name=?", (song1,)))[0][0]
            lyrics2 = list(c.execute("SELECT lyr FROM lyrics WHERE name=?", (song2,)))[0][0]
        except:
            db.close()
            return redirect('/lyrics')
        db.close()

        connections = {}
        lyrics1 = lyrics1.split()
        for j in range(len(lyrics1) - 1):
            word = lyrics1[j]
            nextWords = connections.get(word, [])
            if(len(nextWords) > 0):
                nextWords += [lyrics1[j+1]]
            else:
                connections.update({word: [lyrics1[j+1]]})
        lyrics2 = lyrics2.split()
        for j in range(len(lyrics2) - 1):
            word = lyrics2[j]
            nextWords = connections.get(word, [])
            if(len(nextWords) > 0):
                nextWords += [lyrics2[j+1]]
            else:
                connections.update({word: [lyrics2[j+1]]})

        text = ""
        words = list(connections.keys())
        nextWord = words[random.randint(0, len(words)-1)]
        counter = 0
        while (counter < 180):
            counter += 1
            text += nextWord + " "
            if (counter % 6 == 0):
                text += "<br>"

            try:
                possibleWords = connections[nextWord]
            except:
                possibleWords = connections[words[random.randint(0,len(words)-1)]]

            nextWord = possibleWords[random.randint(0, len(possibleWords)-1)]
        text = text[0].upper() + text[1:]

        return lyrics(mixtext=text)
    return render_template('login.html')

@app.route('/settings', methods = ['GET','POST'])
def settings():
    if 'username' in session:
        value = request.form.to_dict(flat=False)
        global lines
        lines = int(value["lines"][0])
        global similarity
        similarity = int(value["similarity"][0])
        return redirect('/lyrics')
    else:
        return redirect('/home')


@app.route('/song_data', methods = ['GET', 'POST'])
def display_song_data():
    if request.method == 'POST':
        if not request.form['song_name']:
            return render_template('song_data.html', message = "Invalid input")
        else:
            song = request.form['song_name']
            token = get_token()
            result = get_song_features(token, song)
            return render_template('song_data.html', song_data = result)
    return render_template('song_data.html')

@app.route('/visual', methods = ["POST", "GET"])
def visual():
    if request.method == 'POST':
        return render_template('visualizerdata.html')
    else:
        return redirect('/home')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
