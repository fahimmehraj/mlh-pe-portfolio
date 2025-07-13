import os
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
from flask import Flask, render_template, request
from dotenv import load_dotenv

from .experiences import experiences
from .hobbies import hobby_list

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

pages = []
print(os.getcwd())
for filename in os.listdir(os.getcwd() + "/app/templates"):
    if filename.endswith(".html") and filename != "index.html":
        # from the 0th position to the position before 5 from the end,
        # removing the .html extension
        pages.append(filename[:-5])


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        experiences=experiences,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html", title="Hobbies", hobbies=hobby_list, pages=pages
    )


@app.route("/timeline")
def timeline():
    return render_template(
        "timeline.html", title="Timeline", timeline=get_time_line_post()["timeline_posts"], pages=pages
    )
