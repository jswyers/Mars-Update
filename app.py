# import necessary libraries

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo


# create instance of Flask app
app = Flask(__name__)


mongo = PyMongo(app)



@app.route("/scrape")
def scrape():
    mars= mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/",code=302 )
    

# create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)



if __name__ == "__main__":
    app.run(debug=True)
