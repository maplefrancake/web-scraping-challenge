from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_dict"
mongo=PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars)

@app.route("/scrape")
def scraper():
    mars_dict=mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mongo.db.mars_dict.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)