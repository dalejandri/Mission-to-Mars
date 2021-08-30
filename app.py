#The first line says that we'll use Flask to render a template, 
# redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

#The second line says we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

#The third line says that to use the scraping code, 
#we will convert from Jupyter notebook to Python.
import scraping

#set up Flask
app = Flask(__name__)

#connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#set up our Flask routes: one for the main HTML page everyone will view when visiting the web app, 
# and one to actually scrape new data using the code we've written.

#route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#set up our scraping route. This route will be the "button" of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
