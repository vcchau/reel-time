import os 
import time 

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/log")
def log_catch():
    return render_template("log.html")


if __name__ == "__main__":
    app.run(host = "0.0.0.0")