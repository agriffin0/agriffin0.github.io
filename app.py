## import & from statements
import os
import math
# import random
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
from helpers import apology, choose_id, login_required, vinyl, choose_id


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show vinyl collection"""
    
    user_id = session["user_id"]

    # get all unique choices for form
    artist_choices = db.execute("SELECT DISTINCT artist FROM library WHERE user_id=?", user_id)
    genre_choices = db.execute("SELECT DISTINCT genre FROM library WHERE user_id=?", user_id)
    year_choices = db.execute("SELECT DISTINCT decade FROM library WHERE user_id=?", user_id)
    # get library
    libraries = db.execute("SELECT * FROM library WHERE user_id=? ORDER BY artist, year", user_id)
    # get total album count for table
    count_table = db.execute("SELECT COUNT(album) FROM library WHERE user_id=?", user_id)
    count = int(count_table[0]["COUNT(album)"])
    return render_template("index.html", artist_choices=artist_choices, genre_choices=genre_choices, year_choices=year_choices, libraries=libraries, count=count)

# Created for CS50 pset9
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username, password, and confirmation were submitted
        if not username or not password or not confirmation:
            return apology("must provide username, password, and confirmation", 400)

        # ensure password matches confirmatin
        if password != confirmation:
            return apology("password and confirmation must match", 400)

        # if username already taken
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return apology("username already taken", 400)

        # add username and hashed password to table
        rows = db.execute("INSERT INTO users (username, hash) VALUES(? , ?)", username, generate_password_hash(password))

        session["user_id"] = rows

        # log user in
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# Created by CS50
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Created by CS50
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/account")
def account():
    """Display account settings"""

    user_id = session["user_id"]

    return render_template("account.html")

@app.route("/random", methods=["GET", "POST"])
def random():
    """Choose random allbum"""

    user_id = session["user_id"]

    if request.method == "POST":
        
        chosen_artist = request.form.get("artist")
        chosen_genre = request.form.get("genre")
        chosen_year = request.form.get("year")
        if chosen_artist:
            if chosen_genre:
                if chosen_year:
                    # if all 3 criteria
                    options = db.execute("SELECT album, artist FROM library WHERE artist=? AND genre=? AND year=? AND user_id=?", chosen_artist, chosen_genre, chosen_year, user_id)
                    count = len(options) - 1
                    number = randint(0,count)
                    winner = options[number]
                    # return render_template("random.html", count=count, number=number, winner=winner)
                else:
                    # if just artist and genre
                    options = db.execute("SELECT album, artist FROM library WHERE artist=? AND genre=? AND user_id=?", chosen_artist, chosen_genre, user_id)
                    count = len(options) - 1
                    number = randint(0,count)
                    winner = options[number]
                    # return render_template("random.html", count=count, number=number, winner=winner)
            if chosen_year:
                # just artist and year
                options = db.execute("SELECT album, artist FROM library WHERE artist=? AND year=? AND user_id=?", chosen_artist, chosen_year, user_id)
                count = len(options) - 1
                number = randint(0,count)
                winner = options[number]
                # return render_template("random.html", count=count, number=number, winner=winner)
            else:
                # just artist
                options = db.execute("SELECT album, artist FROM library WHERE artist=? AND user_id=?", chosen_artist, user_id)
                count = len(options) - 1
                number = randint(0,count)
                winner = options[number]
                # return render_template("random.html", count=count, number=number, winner=winner)
        # not artist
        elif chosen_genre:
            if chosen_year:
                # just genre and year
                options = db.execute("SELECT album, artist FROM library WHERE genre=? AND year=? AND user_id=?", chosen_genre, chosen_year, user_id)
                count = len(options) - 1
                number = randint(0,count)
                winner = options[number]
                # return render_template("random.html", count=count, number=number, winner=winner)
            else:
                # just genre
                options = db.execute("SELECT album, artist FROM library WHERE genre=? AND user_id=?", chosen_genre, user_id)
                count = len(options) - 1
                number = randint(0,count)
                winner = options[number]
                # return render_template("random.html", count=count, number=number, winner=winner)
        elif chosen_year:
            # just year
            options = db.execute("SELECT album, artist FROM library WHERE year=? AND user_id=?", chosen_year, user_id)
            count = len(options) - 1
            number = randint(0,count)
            winner = options[number]
            # return render_template("random.html", count=count, number=number, winner=winner)
        else:
            # no criteria chosen
            options = db.execute("SELECT album, artist FROM library WHERE user_id=?", user_id)
            count = len(options) - 1
            number = randint(0,count)
            winner = options[number]
            w_album = winner["album"]
            w_artist = winner["artist"]

        return render_template("random.html", count=count, number=number, winner=winner)
    else:
        # get all unique choices for form
        artist_choices = db.execute("SELECT DISTINCT artist FROM library WHERE user_id=?", user_id)
        genre_choices = db.execute("SELECT DISTINCT genre FROM library WHERE user_id=?", user_id)
        year_choices = db.execute("SELECT DISTINCT decade FROM library WHERE user_id=?", user_id)
        return render_template("randomizer.html", artist_choices=artist_choices, genre_choices=genre_choices, year_choices=year_choices)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload album to library table"""

    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        album = request.form.get("album").title()
        artist = request.form.get("artist").title()
        year = request.form.get("year")
        genre = request.form.get("genre")
        if not album or not artist or not year or not genre:
            return apology("Please complete all fields")
        # album already in library
        elif len(db.execute("SELECT album FROM library WHERE album=? AND user_id=?", album, user_id)) != 0:
            return apology("Album has already been added to library")
        elif year.isnumeric() == False:
            return apology("Year must be whole number")
        else:
            # if not new genre
            if len(db.execute("SELECT * FROM library WHERE genre=? AND user_id=?", genre, user_id)) > 0:
                count = db.execute("SELECT count FROM genre_stats WHERE genre=? AND user_id=?", genre, user_id)
                new_count = count[0]["count"] + 1
                db.execute("UPDATE genre_stats SET count=? WHERE genre=? AND user_id=?", new_count, genre, user_id)
            # if new genre
            else:
                new_count = 1
                db.execute("INSERT INTO genre_stats (genre, count, user_id) VALUES(?,?,?)", genre, new_count, user_id)

        # if not new artist
        if len(db.execute("SELECT * FROM library WHERE artist=? AND user_id=?", artist, user_id)) > 0:
            count = db.execute("SELECT count FROM artist_stats WHERE artist=? AND user_id=?", artist, user_id)
            new_count = count[0]["count"] + 1
            db.execute("UPDATE artist_stats SET count=? WHERE artist=? AND user_id=?", new_count, artist, user_id)
        # if new artist
        else:
            new_count = 1
            db.execute("INSERT INTO artist_stats (artist, count, user_id) VALUES(?,?,?)", artist, new_count, user_id)
                
        decade = math.floor(int(year)/10) * 10
        db.execute("INSERT INTO library (artist, album, year, genre, decade, user_id) VALUES (?,?,?,?,?,?)", artist, album, year, genre, decade, user_id)    
        # add to account
        return redirect("/")
    else:
        return render_template("upload.html")

@app.route("/stats")
def stats():
    """Display collection statistics"""

    user_id = session["user_id"]

    # table of genre count
    # pull data
    stats = db.execute("SELECT * FROM genre_stats WHERE user_id=? ORDER BY count DESC", user_id)

    # get total album count for table
    count_table = db.execute("SELECT COUNT(album) FROM library WHERE user_id=?", user_id)
    count = int(count_table[0]["COUNT(album)"])


    # list of top artists
    artists = db.execute("SELECT * FROM artist_stats WHERE user_id=? ORDER BY count DESC", user_id)
    artist_count_table = db.execute("SELECT COUNT(artist) FROM library WHERE user_id=?", user_id)
    artist_count = int(artist_count_table[0]["COUNT(artist)"])

    return render_template("stats.html", stats=stats, count=count, artists=artists, artist_count=artist_count)

@app.route("/counter", methods=["GET", "POST"])
def counter():
    """Keep count of listening history"""

    user_id = session["user_id"]

    if request.method == "POST":
        album = request.form.get("album")
        if len(db.execute("SELECT * FROM listen_count WHERE album=? AND user_id=?", album, user_id)) != 0:
            count_table = db.execute("SELECT count FROM listen_count WHERE album=? AND user_id=?", album, user_id)
            count = int(count_table[0]["count"]) + 1
            db.execute("UPDATE listen_count SET count=? WHERE album=? AND user_id=?", count, album, user_id)
        else:
            count = 1
            db.execute("INSERT INTO listen_count(album, count, user_id) VALUES(?,?,?)", album, count, user_id)
        db.execute("INSERT INTO listen_history(album, user_id) VALUES(?,?)", album, user_id)
        return redirect("/counter")
    else:
        albums = db.execute("SELECT album FROM library WHERE user_id=?", user_id)
        counts = db.execute("SELECT * FROM listen_count WHERE user_id=? ORDER BY count DESC", user_id)
        return render_template("counter.html", albums=albums, counts=counts)