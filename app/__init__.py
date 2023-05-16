from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from spotify_api import *

app = Flask(__name__)
app.secret_key = os.urandom(32) # This is NOT secure

@app.route('/')
def log_in():
    if 'username' in session: # If already logged in
        return redirect('/home')
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
        return render_template('profile.html', message = message,Username = session['username'])
    return render_template('profile.html')

@app.route('/artist', methods = ['GET', 'POST'])
def artist():
    if request.method == 'POST':
        artist = request.form['artist_name']
        token = get_token()
        result = search_for_artist(token, artist)
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)
        return render_template('artist.html', data = songs)
    return render_template('artist.html')

@app.route('/lyrics' , methods = ['GET', 'POST'])
def lyrics():
    return render_template('lyrics.html')


if __name__ == "__main__":
  app.run(debug=True)
