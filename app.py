from time import time
from random import sample, choice, randint
from cs50 import SQL
from flask import Flask, redirect, render_template, request, g

colors = ["pink", "blue", "black", "green", "brown", "yellow", "red", "purple", "orange"]
colors_two = ["pink", "blue", "black", "green", "brown", "yellow", "red", "purple", "orange"]
colors_three = ["pink", "blue", "black", "green", "brown", "yellow", "red", "purple", "orange"]
templates = ["pink.html", "blue.html", "black.html", "green.html", "brown.html", "yellow.html", "red.html", "purple.html", "orange.html"]
start_time = None
color_choice = None
random_results = {}
num = None
# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///results.db")

@app.before_request
def before_request():
   g.request_start_time = time()
   g.request_time = time() - g.request_start_time

# The setup of the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    global num
    # Render the homepage
    if request.method == "GET":
        return render_template("index.html")
    else:
        num = randint(0,1)
        if num == 0:
            return redirect("/form_one")
        else:
            return redirect("/form_two")

@app.route("/form_one", methods=["GET", "POST"])
def form_one():
    global start_time
    global color_choice
    global num
    # Render the slide
    if request.method == "GET":

        if len(colors) != 0:
            color_choice = choice(colors)
            template = choice(templates)
            alt_color = template.removesuffix(".html")

            if color_choice + ".html" == template:
                return redirect("/form_one")

            colors.remove(color_choice)
            templates.remove(template)

        else:
            db.execute("INSERT INTO randomized (black, blue, brown, green, orange, pink, purple, red, yellow) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", random_results['black'], random_results['blue'], random_results['brown'], random_results['green'], random_results['orange'], random_results['pink'], random_results['purple'], random_results['red'], random_results['yellow'])
            if num == 0:
                return redirect("/form_two")
            else:
                return render_template("end.html")

        ordering = sample([color_choice, alt_color], k=2)

        start_time = time()

        return render_template(template, word_one = ordering[0], form = "/form_one", word_two = ordering[1], word = color_choice)

    else:
        total_time = (time() - start_time) - g.request_time

        if request.form[color_choice] == color_choice:
            random_results[color_choice] = total_time
        else:
            random_results[color_choice] = None

        return redirect("/form_one")

@app.route("/form_two", methods=["GET", "POST"])
def form_two():
    global start_time
    global color_choice
    global num
    if request.method == "GET":

        if len(colors_two) != 0:
            color_choice = choice(colors_two)
            colors_two.remove(color_choice)
            colors_four = colors_three.copy()
            colors_four.remove(color_choice)
            alt_color = choice(colors_four)
        else:
            db.execute("INSERT INTO ordered (black, blue, brown, green, orange, pink, purple, red, yellow) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", random_results['black'], random_results['blue'], random_results['brown'], random_results['green'], random_results['orange'], random_results['pink'], random_results['purple'], random_results['red'], random_results['yellow'])
            if num == 0:
                return render_template("end.html")
            else:
                return redirect("/form_one")

        ordering = sample([color_choice, alt_color], k=2)

        start_time = time ()

        return render_template(color_choice + ".html", word_one = ordering[0], form = "/form_two", word_two = ordering[1], word = color_choice)

    else:
        total_time = (time() - start_time) - g.request_time

        if request.form[color_choice] == color_choice:
            random_results[color_choice] = total_time
        else:
            random_results[color_choice] = None

        return redirect("/form_two")
