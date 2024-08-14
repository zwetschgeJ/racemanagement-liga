import pandas as pd
from pymongo.mongo_client import MongoClient

from src.utils_app import get_data_google

from config import *

# Replace with your MongoDB URI
uri = "mongodb+srv://antonsattler:ahD84bgTF2dNtUqn@cluster0.3rpqm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Get data
df = get_data_google(link_id=link_event_01, stupid_formatting=True)

# Select your database and collection
db = client["event01"]  # replace with your database name
collection = db["dsbl"]  # replace with your collection name

# Convert the DataFrame to a list of dictionaries
data_dict = df.to_dict("records")

# Insert the data into the collection
try:
    collection.insert_many(data_dict)
    print("DataFrame inserted successfully!")
except Exception as e:
    print("An error occurred while inserting the data:", e)
