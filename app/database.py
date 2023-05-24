import sqlite3

db = sqlite3.connect("user.db", check_same_thread=False) #CRUCIAL
global c
c = db.cursor()

# making tables
c.execute("CREATE TABLE if not exists users(username TEXT, password TEXT)")

# general method that can be used to get data easier
def select_from(database, table, data_want, datagive, datatype_give):
    db = sqlite3.connect(database, check_same_thread=False)
    c = db.cursor()
    temp = ((c.execute(f"SELECT {data_want} FROM {table} WHERE {datatype_give} = '{datagive}'")).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0

def username_in_system(username):
    db = sqlite3.connect("user.db", check_same_thread=False)
    c = db.cursor()
    temp = list(c.execute("SELECT username FROM users").fetchall())
    for element in temp:
        for element2 in element:
            if username == element2:
                return True
    return False

def signup(username, password):
    db = sqlite3.connect("user.db", check_same_thread=False)
    c = db.cursor()
    if(username_in_system(username)):
        return False
    else:
        c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    db.commit()
    return True #save changes

def remove_user(username):
    db = sqlite3.connect("user.db", check_same_thread=False)
    c = db.cursor()
    try:
        c.execute(f'DELETE FROM users WHERE username = "{username}"')
        db.commit()
        return True
    except:
        return False

# to verify if the password given is right to login
def login(username, password):
    db = sqlite3.connect("user.db")
    c = db.cursor()
    if(username_in_system(username)):
        if(select_from("user.db", "users", "password", username, "username") == password):
            return True
    return False

def DB_changepw(username, newpassword):
    db = sqlite3.connect("user.db", check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE users SET password =? WHERE username =?", (newpassword, username))
    db.commit()
    return "New password saved!" #save changes

db.commit()
db.close()
