import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from .experiences import experiences

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), experiences=experiences)
