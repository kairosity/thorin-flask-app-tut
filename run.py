import os
import json
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env


# creating an instance of the Flask class and storing it in a
# var called app. The first param of the flask class is the name
# of the apps module. __name__ is a built in python var.
# Flask needs __name__ so it knows where to look for templates & static files.
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


# The route @decorator tells flask what URL should trigger the function
# that follows decorators wrap functions.
@app.route("/")
def index():
    return render_template('index.html')


# the function that is triggered below the route is also called a "View".
@app.route("/about")
def about():
    data = []
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", company=data)


# Any time we look at the about url with something after it - whatever comes
# after it will be passed into this view.
@app.route("/about/<member_name>")
def about_member(member_name):
    member = {}
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return render_template("member.html", member=member)
    # first member is the var we created INSIDE the member.html file.
    # second member is the member above that holds the json data.


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    return render_template("contact.html", page_title="Contact")


@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")


# Python assigns the name "__main__" to the script when the script
# is executed. Therefore, __name__ will be equal to "__main__".
# That means the if conditional statement is satisfied and the app.run()
# method will be executed.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

