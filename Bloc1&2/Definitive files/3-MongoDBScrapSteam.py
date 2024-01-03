import csv
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://admin:admin@cluster0.nzzgzi7.mongodb.net/')  # Replace with your MongoDB connection string
db = client['SteamDB']  # Replace with the desired database name

# Create a new collection
collection = db['SteamInfosGames']  # Replace with the desired collection name

# Read CSV file and insert into the collection
with open('steam_data2.csv', 'r', encoding='utf-8-sig') as csvfile:  # Replace with the path to your CSV file
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        collection.insert_one(row)

