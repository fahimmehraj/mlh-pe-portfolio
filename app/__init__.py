import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from .experiences import experiences
from .hobbies import hobby_list

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), experiences=experiences)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=hobby_list)
