from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *

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



@app.route('/lyrics', methods = ['GET','POST'])
def lyrics(*text):
    if 'username' in session: # If already logged in
        if (len(text) == 0): #weird handling?
            text = ""
        print(lines)
        return render_template('lyrics.html', newText = text, dLines = lines, dSim = similarity)
    return render_template('login.html')

@app.route('/generate', methods = ['GET','POST'])
def generate():
    return redirect('/lyrics')

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
