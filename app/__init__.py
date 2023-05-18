from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from spotify_api import *

app = Flask(__name__)
app.secret_key = os.urandom(32) # This is NOT secure

# For lyric generation
lines = 30
similarity = 1

@app.route('/')
def log_in():
    global lines, similarity
    lines = 30
    similarity = 1
    if 'username' in session: # If already logged in
        return redirect('/home', user = session["username"])
    return render_template('login.html') # For login AND signup

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if (session): # If logged in, show the home page
        return render_template('home.html', user = session['username'])
    else: # ...else show the login page
        return redirect('/')

@app.route('/login', methods = ["POST"])
def authenticate():
    if 'username' in session:
        return render_template('home.html', user = 'username')
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['password']
    if login(user,pw):
        if request.method == 'POST':
            session['username'] = request.form['username']
        if request.method == 'GET':
            session['username'] = request.args['username']
        return redirect('/home')
    else:
        return render_template('login.html', errorTextL= "Please enter a valid username and password")

@app.route('/signup', methods = ["POST"])
def sign_up():
    if 'username' in session:
        return render_template('home.html', user = 'username')
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        email = request.form['email']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['password']
        email = request.args['email']
    if '@' in email and '.' in email.split('@')[1]:
        if signup(user,pw,email):
            return render_template('login.html')
        else:
            return render_template('login.html', errorTextS= "User already exists")
    else:
        return render_template('login.html', errorTextS = "Invalid email")

@app.route('/profile', methods = ['POST','GET'])
def profile():
    if 'username' in session:
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

@app.route('/artist', methods = ['GET', 'POST'])
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
    return render_template('artist.html')


@app.route('/lyrics', methods = ['GET','POST'])
def lyrics(*text):
    if 'username' in session: # If already logged in
        if (len(text) == 0): #weird handling?
            text = ""
        return render_template('lyrics.html', newText = text, dLines = lines, dSim = similarity)
    return render_template('login.html')

@app.route('/generate', methods = ['GET','POST'])
def generate():
    data = open("./lyrics/data.txt", "r")
    data = json.load(data)
    print(len(data))

    text = ""
    for i in range(lines * 8): #words per line
        text += ""

    return lyrics(text) #weird?

@app.route('/settings', methods = ['GET','POST'])
def settings():
    value = request.form.to_dict(flat=False)
    global lines
    lines = value["lines"][0]
    global similarity
    similarity = value["similarity"][0]
    return redirect('/lyrics')


if __name__ == "__main__":
  app.run(debug=True)
