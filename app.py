from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from scrape_mars import scrape
import pymongo

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mission_to_mars
# db.mars.drop()
# mars_dict = scrape()
# db.mars.insert_one(mars_dict)

# Set route
@app.route('/')
def index():
    mars_page = db.mars.find_one()
    return render_template('index.html', mars=mars_page)

@app.route('/launch')
def launch():
    db.mars.drop()
    mars_dict = scrape()
    db.mars.insert_one(mars_dict)
    mars_page = db.mars.find_one()

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars_page)


if __name__ == "__main__":
    app.run(debug=True)
