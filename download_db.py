import pandas as pd
from pymongo.mongo_client import MongoClient

# Replace with your MongoDB URI
uri = "mongodb+srv://antonsattler:ahD84bgTF2dNtUqn@cluster0.3rpqm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select your database and collection
db = client["event01"]  # replace with your database name
collection = db["dsbl"]  # replace with your collection name

# Load data from MongoDB collection into a pandas DataFrame
try:
    data = list(collection.find())  # Fetch all documents from the collection
    df = pd.DataFrame(data)  # Convert list of documents to DataFrame

    # Optionally, drop the '_id' column (if it's not needed)
    if '_id' in df.columns:
        df = df.drop('_id', axis=1)

    print("Data loaded into DataFrame successfully!")
    print(df)
except Exception as e:
    print("An error occurred while loading the data:", e)
