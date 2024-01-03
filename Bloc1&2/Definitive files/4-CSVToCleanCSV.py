import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from pymongo.operations import UpdateOne

input_file = 'C:/Users/mathi/VsCodeRepo/Steam-games-overview-Prj/Bloc1&2\Definitive files\TEST\steam_data2.csv'
output_file = 'C:/Users/mathi/VsCodeRepo/Steam-games-overview-Prj/Bloc1&2\Definitive files\TEST\data_clean.csv'


# STEP 1 : Eliminer tous les caractères spéciaux indésirables et restructuer le fichier pour avoir 1 ligne = 1 enregistrement
print("STEP 1 Starting ...")
def clean_CSV(input_text):
    # Use BeautifulSoup to parse and remove HTML tags
    soup = BeautifulSoup(input_text, 'html.parser')
    clean_text = soup.get_text()

    # Remove characters not in AZERTY keyboard layout
    clean_text = re.sub(r'[^a-zA-Z0-9\séèçàêîôû\'"\-.,;:!@#~&\[\]\(\)_+=<>?/|\\%]', '', clean_text)
    #Replace multiple white spaces by one only
    clean_text = re.sub(r'\s+', ' ', clean_text)

    return clean_text

with open(input_file, 'r', encoding='utf-8') as infile, \
        open(output_file, 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        cleaned_row = [clean_CSV(cell) for cell in row]
        processed_row = [cell.replace('\n', ' ') for cell in cleaned_row]  # Replace newline with space
        writer.writerow(processed_row)

print(f"Processed CSV saved to '{output_file}'.")

#############################################################################################################
# STEP 2 : restructurer les champs nécessaires avec pandas
print("STEP 2 Starting ...")

# Read the CSV file
df = pd.read_csv('Bloc1&2\Definitive files\TEST\data_clean.csv')

# Define a function to extract configurations
def extract_configurations_configurations(row):
    # Remove all backslashes from the row
    row = row.replace("\\", "")
    
    config_pattern = re.compile(r"'minimum': '(.*?)', 'recommended': '(.*?)'")
    match = config_pattern.search(row)
    if match:
        minimal = match.group(1)
        recommended = match.group(2)
        return minimal, recommended
    elif "'minimum': '" in row:
        minimal = re.search(r"'minimum': '(.*?)'", row).group(1)
        return minimal, ''
    elif "'minimum': \"" in row:
        minimal = re.search(r"'minimum': \"(.*?)\"", row).group(1)
        return minimal, ''
    elif "'recommended':" in row:
        recommended = re.search(r"'recommended': '(.*?)'", row).group(1)
        return '', recommended
    else:
        return '', ''

# Define a function to extract configurations
def extract_configurations_plateformes(row):
    config_pattern = re.compile(r"'windows': (\w+), 'mac': (\w+), 'linux': (\w+)")
    match = config_pattern.search(row)
    if match:
        windows = match.group(1)
        mac = match.group(2)
        linux = match.group(3)
        return windows, mac, linux

# Extract configurations and store in separate lists
min_configurations = []
rec_configurations = []
windowsCol = []
macCol = []
linuxCol = []

for row in df['Configurations recommandées']:
    minimal, recommended = extract_configurations_configurations(row)
    min_configurations.append(minimal)
    rec_configurations.append(recommended)

for row in df['Plateformes']:
    windows, mac, linux = extract_configurations_plateformes(row)
    windowsCol.append(windows)
    macCol.append(mac)
    linuxCol.append(linux)

# Create new columns and populate them with extracted data
df['Configurations minimales'] = min_configurations
df['Configurations recommandées'] = rec_configurations
df['Windows'] = windowsCol
df['Mac'] = macCol
df['Linux'] = linuxCol

# Replace NaN in 'price infos' with 'Free To Play' where 'Gratuit' is True
df.loc[df['Gratuit'] == True, 'Price infos'] = df.loc[df['Gratuit'] == True, 'Price infos'].fillna('Free To Play')

# Replace NaN in 'price infos' with 'Non renseigné' where 'Gratuit' is False
df.loc[df['Gratuit'] == False, 'Price infos'] = df.loc[df['Gratuit'] == False, 'Price infos'].fillna('Non renseigné')

# Split the column into two separate columns
df['coming_soon'] = df['Date de parution'].str.extract(r"'coming_soon': (.*?),")
df['date_de_parution'] = df['Date de parution'].str.extract(r"'date': '(.*?)'")

# Drop the original 'coming_soon_date' column
df.drop(columns=['Date de parution'], inplace=True)


# Split the 'Metacritic' column into two separate columns
df['Metacritic score'] = df['Metacritic'].str.extract(r"'score': (.*?),")
df['Metacritic url'] = df['Metacritic'].str.extract(r"'url': '(.*?)'")

# Drop the original column 
df.drop(columns=['Plateformes'], inplace=True)
df.drop(columns=['Metacritic'], inplace=True)

#Create a Rank from indexId
df['Rang'] = list(range(1, len(df) + 1))   

# Save the modified DataFrame to a new CSV file
df.to_csv('Bloc1&2\Definitive files\TEST\data_clean2.csv', index=False)

#############################################################################################################
# STEP 3 : Upload les fichiers CSV dans une DB mongo afin de pouvoir les manipuler dans l'étape 4
print("STEP 3 Starting ...")

# Connect to MongoDB
client = MongoClient('mongodb+srv://hydronalpha:hydronalpha@cluster0.u4etida.mongodb.net/')  # Replace with your MongoDB connection string
db = client['TESTSteamDBtest']  # Replace with the desired database name

# Create a new collection
collection = db['SteamInfosGamestest']  # Replace with the desired collection name

# Read CSV file and insert into the collection
with open('Bloc1&2\Definitive files\TEST\data_clean2.csv', 'r', encoding='utf-8-sig') as csvfile:  # Replace with the path to your CSV file
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        collection.insert_one(row)

# Close the connection
client.close()

#############################################################################################################
# STEP 4 : Restructurer d'autres champs avec mongo pour améliorer la lisibité et la maniabilité des données
print("STEP 4 Starting ...")

# Connect to MongoDB // Vérifier la correspondance des noms de la db et de la collection avec l'étape 3
client = MongoClient('mongodb+srv://hydronalpha:hydronalpha@cluster0.u4etida.mongodb.net/')  # Replace with your MongoDB connection string
db = client['TESTSteamDBtest']  # Replace with the desired database name

# Create a new collection
collection = db['SteamInfosGamestest']  # Replace with the desired collection name"

# Regular expression pattern to match description values
pattern = r"'description': '([^']+)'"  # Matches text within single quotes after "'description': '"

# Iterate through documents and update the "Genres" field
for document in collection.find():
    genres_str = document.get("Genres", "")
    descriptions = re.findall(pattern, genres_str)
    collection.update_one(
        {"_id": document["_id"]},
        {"$set": {"Genres": descriptions}}
    )

# Iterate through documents and update the "Categories" field
for document in collection.find():
    categories_str = document.get("Categories", "")
    descriptions = re.findall(pattern, categories_str)
    collection.update_one(
        {"_id": document["_id"]},
        {"$set": {"Categories": descriptions}}
    )    

# Iterate through documents and update the "Développeur" field
for document in collection.find():
    developer_str = document.get("Développeur", "")
    try:
        developer_list = eval(developer_str)
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"Développeur": developer_list}}
        )
    except (SyntaxError, TypeError):
        # Handle cases where "Développeur" string can't be evaluated
        pass

# Iterate through documents and update the "Éditeur" field
for document in collection.find():
    developer_str = document.get("Éditeur", "")
    try:
        developer_list = eval(developer_str)
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"Éditeur": developer_list}}
        )
    except (SyntaxError, TypeError):
        # Handle cases where "Éditeur" string can't be evaluated
        pass



# Iterate through documents and update the "Langages supportés" field
supported_languages = ['Czech', 'Danish', 'Dutch', 'English', 'Finnish', 'French', 'German', 'Hungarian', 'Italian', 'Japanese', 'Korean', 'Norwegian', 'Polish', 'Portuguese - Portugal', 'Portuguese - Brazil', 'Romanian', 'Russian', 'Simplified Chinese', 'Spanish - Spain', 'Swedish', 'Thai', 'Traditional Chinese', 'Turkish', 'Bulgarian', 'Ukrainian', 'Greek', 'Spanish - Latin America', 'Vietnameselanguages with full audio support', 'Arabiclanguages with full audio support', 'Arabic', 'Ukrainianlanguages with full audio support', 'Spanish - Latin Americalanguages with full audio support', 'Indonesian', 'Persian', 'Portuguese - Brazillanguages with full audio support', 'Vietnamese', 'Thailanguages with full audio support', 'Traditional Chineselanguages with full audio support', 'Romanianlanguages with full audio support', 'Spanish - Spainlanguages with full audio support', 'Simplified Chineselanguages with full audio support', 'Koreanlanguages with full audio support', 
                       'Japaneselanguages with full audio support', 'Turkishlanguages with full audio support', 'Indonesianlanguages with full audio support', 'Germanlanguages with full audio support', 'Hindi', 'Malaylanguages with full audio support', 'Polishlanguages with full audio support', 'Englishlanguages with full audio support', 'Belarusian', 'Catalan', 'Kazakh', 'Georgian', 'Russianlanguages with full audio support', 'Italianlanguages with full audio support', 'Hindilanguages with full audio support', 'Catalanlanguages with full audio support', 'Armenian', 'Basque', 'Estonian', 'Filipino', 'Galician', 'Hebrew', 'Malay', 'Slovak', 'Slovenian', 'Swedishlanguages with full audio support', 'Czechlanguages with full audio support', 'Latvian', 'Lithuanian', 'Slovaklanguages with full audio support', 'Serbianlanguages with full audio support', 'Serbian', 'Portuguese - Portugallanguages with full audio support', 'Croatian', 'Lithuanianlanguages with full audio support', 'Frenchlanguages with full audio support', 'Croatianlanguages with full audio support', 'Greeklanguages with full audio support', 'Hungarianlanguages with full audio support', 'Hebrewlanguages with full audio support', 'Afrikaans', 'Finnishlanguages with full audio support', 'Dutchlanguages with full audio support', 
                       'Afrikaanslanguages with full audio support', 'Traditional Chinese (text only)']


# Create a list of update operations using bulk write
bulk_updates = []

# Iterate through documents and update the "Langages supportés" field
for document in collection.find():
    supported_languages_present = document.get("Langages supportés", [])
    update_data = {}
    for language in supported_languages:
        update_data[language] = language in supported_languages_present

    bulk_updates.append(
        UpdateOne({"_id": document["_id"]}, {"$set": update_data})
    )

# Execute the bulk write operations
if bulk_updates:
    collection.bulk_write(bulk_updates)

# Delete the "Langages supportés" field from all documents
collection.update_many({}, {"$unset": {"Langages supportés": ""}})

# Close the connection
client.close()