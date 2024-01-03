import pymongo
import pandas as pd

# Connect to MongoDB // Vérifier la correspondance des noms de la db et de la collection avec l'étape 3
client = pymongo.MongoClient('mongodb+srv://hydronalpha:hydronalpha@cluster0.u4etida.mongodb.net/')  # Replace with your MongoDB connection string
db = client['TESTSteamDBtest']  # Replace with the desired database name

# Create a new collection
collection = db['SteamInfosGamestest']  # Replace with the desired collection name"

# Fetch documents from the collection
documents = collection.find({}, {"_id": 0}) # You can add filters here if needed

# Convert documents to a pandas DataFrame
df = pd.DataFrame(documents)

# Save DataFrame as CSV file
csv_filename = "Bloc1&2\Definitive files\TEST\\testMongoToCSV.csv"  # Change to your desired filename
df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' created.")