## Jason Johnson was here.

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#################################################
# Flask Routes
#################################################


@app.route("/")
def index():
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.replace_one({},data,upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run()