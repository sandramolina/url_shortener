from flask import Flask, render_template, request, redirect, url_for
import json
import os.path

app = Flask(__name__)

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
            return redirect(url_for("home"))

        user_urls[request.form['code']] = {"url":request.form['url']}
        with open("user_urls.json", "w") as url_file: #"w" - Write - Opens a file for writing, creates the file if it does not exist
        #The "as" keyword is used to create an alias.
            json.dump(user_urls, url_file)
        return render_template('your_url.html', code=request.form['code']) #code is the short name we want to give to the shorten url (input tag in home.html)

    else:
        return redirect(url_for("home")) #this will take the user to the home page it the your url is tried to be accessed from the url bar