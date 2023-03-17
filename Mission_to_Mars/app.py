from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mongo.db.mars_dict.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)