from flask import Flask,render_template,redirect,request
import requests
#from autoscraper import Autoscraper
from bs4 import BeautifulSoup
import pandas as pd

application = Flask(__name__)
app = application
@app.route("/",methods=["POST","GET"])
def index():
    product_details = []
    if request.method=="POST":
        product_name = request.form["product_name"]
        product_details=get_product_details(product_name)
    return render_template("index.html",product_details=product_details)


def get_product_details(product_name):
    url = f"https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    names = soup.find_all("div",class_="_4rR01T")
    products = [name.text for name in names]
    ratingss = soup.find_all("div",class_ ="_3LWZlK" )
    ratings = [rating.text for rating in ratingss]
    price = soup.find_all("div",class_="_30jeq3 _1_WHN1") 
    prices = [rate.text for rate in price ]
    ratings=ratings[:24]
    
    
    
    df = pd.DataFrame({"Product Name": products, "Price": prices, "Rating": ratings})
    return df.to_dict("records")
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5050)
    