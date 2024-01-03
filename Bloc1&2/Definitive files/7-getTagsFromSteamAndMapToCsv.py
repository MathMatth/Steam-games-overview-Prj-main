import csv
from bs4 import BeautifulSoup
import requests 
import re
import pandas as pd


###############################################################################################
#
# Utiliser l'ID steam des jeux afin de récupérer et de mapper les tags steam correspondants
#
###############################################################################################

urlAppDetails = "https://store.steampowered.com/app/"
game_Ids_and_names = {}
game_Ids_and_tags = {}

# Ouvre le csv avec les ID des jeux que l'ont veux récup
with open('Bloc1&2\Definitive files\TEST\steam_data.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    # Skip the header row
    next(csv_reader)
    # Iterate through the rows and extract IDs
    for row in csv_reader:
        game_id = row[0]  # ID is the first column
        game_name = row[1]  # Name is the second column
        new_key_values_itr = [(game_id,game_name)]
        game_Ids_and_names.update(new_key_values_itr)

    for game in game_Ids_and_names.items():
        urlToCall = urlAppDetails + game[0] + '/' + game[1]
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(urlToCall).text
        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")
        #print(soup.prettify()) # print the parsed data of html
        pattern = re.compile(r'"tagid":\d+,"name":"(.*?)"')
        matches = pattern.findall(html_content)
        result = [(name) for name in matches]
        game_and_tags_itr = [(game[0],result)]
        game_Ids_and_tags.update(game_and_tags_itr)
        print(game_and_tags_itr)

print("Starting Mapping tags")

df = pd.read_csv("Bloc1&2\Definitive files\TEST\\testMongoToCSV.csv")

#for item in game_Ids_and_tags.items():
#    item[0] #ID steam du jeu
#    item[1] #Liste des tags du jeu
#game_Ids_and_tags = []
#game_Ids_and_tags.append({"730" : ["bla", "bli","blo"]})
    
# Define a function to map the values from the dictionary to the "Genres" column
def map_genres(id):
    for elementId in game_Ids_and_tags:
        if str(id) in game_Ids_and_tags.keys():
            return ', '.join(game_Ids_and_tags[str(id)])
        return ''

# Apply the function to update the "Genres" column
df['Genres'] = df['ID'].map(map_genres) 

# Save the updated DataFrame back to a CSV file if needed
df.to_csv('Bloc1&2\Definitive files\TEST\data_clean3_with_SteamTags.csv', index=False)