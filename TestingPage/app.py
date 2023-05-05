from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home")
def correct():
    return render_template("correct.html")

app.run("127.0.0.1", port=8000)