from flask import Flask, render_template, request
from sg_ccentric import check_code_c_centric
from waitress import serve
from datetime import datetime
from dotenv import load_dotenv
import os

from pymongo import MongoClient
import pymongo

# Load environment variables from .env file
load_dotenv()

# Access environment variables
USERNAME1 = os.environ.get("USERNAME1")
SECRET = os.environ.get("SECRET")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

app = Flask(__name__)
# Establish connection to MongoDB
#client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
# Use credentials to connect to MongoDB
uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@10.131.1.106/?authSource=admin"
client = MongoClient(uri)

db = client["local"]  # Replace "your_database_name" with your actual database name
collection = db["Imeis_C_Centric"]  # Replace "your_collection_name" with your actual collection name

# Function to get current date and time
def get_current_date():
    return datetime.now()

# MongoDB URI
#uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5"

try:
    # Connect to MongoDB
    #client = pymongo.MongoClient(uri)

    # Check if connection is successful
    db_names = client.list_database_names()
    print("Connected to MongoDB")
    print("Available databases:")
    for db_name in db_names:
        print(db_name)

except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/ccentric')
def get_code():
    imei = request.args.get('imei' ,'')
    # Check if the IMEI is a numeric value and has a length of 15
    if imei.isdigit() and len(imei) == 15:
        result_code_c_centric = check_code_c_centric(imei)
         # Insert IMEI into MongoDB collection
        #data = {"imei": imei, "result": result_code_c_centric}
        #collection.insert_one(data)
        # Add current date to the data
        current_date = get_current_date().strftime("%Y-%m-%dT%H:%M")
        data = {
            "imei": imei,
            "result": result_code_c_centric,
            "date_added": current_date  # Add date field,
            }
        try:
            collection.insert_one(data)
        except errors.PyMongoError as e:
            print(f"Error inserting data into MongoDB: {e}")
        print(imei)
        print(result_code_c_centric)
        return render_template(
            "ccentric.html",
            imei=imei,  # Pass imei to the template
            result = result_code_c_centric
        )
        client.close()

    else:
        return render_template("invalid_imei.html")
    
    
    
@app.teardown_appcontext
def close_connection(exception):
    client.close()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)