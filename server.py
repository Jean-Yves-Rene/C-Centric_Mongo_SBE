from flask import Flask, render_template, request
from sg_ccentric import check_code_c_centric
from waitress import serve
from datetime import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient, errors

# Load environment variables from .env file
load_dotenv()

# Access environment variables
USERNAME1 = os.environ.get("USERNAME1")
SECRET = os.environ.get("SECRET")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

app = Flask(__name__)

# Establish connection to MongoDB using credentials
# uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@10.131.1.106/?authSource=admin"
# client = None

# try:
#     client = MongoClient(uri)
#     # Check if connection is successful
#     db_names = client.list_database_names()
#     print("Connected to MongoDB")
#     print("Available databases:")
#     for db_name in db_names:
#         print(db_name)
# except errors.ConnectionFailure as e:
#     print("Could not connect to MongoDB:", e)
#     client = None

# if client:
#     db = client["local"]  # Replace with your actual database name
#     collection = db["Imeis_C_Centric"]  # Replace with your actual collection name

# Function to get current date and time
def get_current_date():
    return datetime.now()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/ccentric')
def get_code():
    imei = request.args.get('imei', '')
    # Check if the IMEI is a numeric value and has a length of 15
    if imei.isdigit() and len(imei) == 15:
        result_code_c_centric = check_code_c_centric(imei)
        # Add current date to the data
        current_date = get_current_date().strftime("%Y-%m-%dT%H:%M")
        data = {
            "imei": imei,
            "result": result_code_c_centric,
            "date_added": current_date  # Add date field
        }
        # Insert IMEI into MongoDB collection if client is connected
        # if client:
        #     collection.insert_one(data)
        return render_template(
            "ccentric.html",
            imei=imei,  # Pass imei to the template
            result=result_code_c_centric
        )
    else:
        return render_template("invalid_imei.html")

# Gracefully disconnect from MongoDB when the application exits
# @app.teardown_appcontext
# def close_connection(exception):
#     if client:
#         client.close()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
