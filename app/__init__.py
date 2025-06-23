import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from .experiences import experiences
from .hobbies import hobby_list

load_dotenv()
app = Flask(__name__)

pages = []
print(os.getcwd())
for filename in os.listdir(os.getcwd() + "/app/templates"):
    if filename.endswith('.html') and filename != "index.html":
        # from the 0th position to the position before 5 from the end,
        # removing the .html extension
        pages.append(filename[:-5])


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), experiences=experiences, pages=pages)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=hobby_list, pages=pages)
