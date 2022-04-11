from fileinput import filename
import re
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "423423dfbfelfdmbl566750376bgb"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/your-url', methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        user_urls = {}

        if os.path.exists("user_urls.json"):
            with open("user_urls.json") as urls_file:
                    user_urls = json.load(urls_file)

        if request.form["code"] in user_urls.keys():
            flash("Short name taken, please create another one")
            return redirect(url_for("home"))

        if "url" in request.form.keys():
            user_urls[request.form['code']] = {"url":request.form['url']}

        else:
            f = request.files["file"]
            full_name = request.form["code"] + secure_filename(f.filename)
            f.save("/Users/sandra/Documents/Dev 1/python/url_shortener/static/user_files/" + full_name)
            user_urls[request.form['code']] = {"file":full_name}
        
        with open("user_urls.json", "w") as url_file: #"w" - Write - Opens a file for writing, creates the file if it does not exist
        #The "as" keyword is used to create an alias.
            json.dump(user_urls, url_file)
        return render_template('your_url.html', code=request.form['code']) #code is the short name we want to give to the shorten url (input tag in home.html)

    else:
        return redirect(url_for("home")) #this will take the user to the home page it the your url is tried to be accessed from the url bar

@app.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("user_urls.json"):
        with open("user_urls.json") as urls_file:
            user_urls = json.load(urls_file)
            if code in user_urls.keys():
                if "url" in user_urls[code].keys():
                    return redirect(user_urls[code]["url"])
                else:
                    return redirect(url_for("static", filename="user_files/" + user_urls[code]["file"]))


