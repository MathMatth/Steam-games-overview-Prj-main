supported_languages = ['Czech' 'Danish' 'Dutch' 'English' 'Finnish' 'French' 'German' 'Hungarian' 'Italian' 'Japanese' 'Korean' 'Norwegian' 'Polish'
 'Portuguese - Portugal' 'Portuguese - Brazil' 'Romanian' 'Russian'     
 'Simplified Chinese' 'Spanish - Spain' 'Swedish' 'Thai'
 'Traditional Chinese' 'Turkish' 'Bulgarian' 'Ukrainian' 'Greek'        
 'Spanish - Latin America' 'Vietnameselanguages with full audio support'
 'Arabiclanguages with full audio support' 'Arabic'
 'Ukrainianlanguages with full audio support'
 'Spanish - Latin Americalanguages with full audio support' 'Indonesian'
 'Persian' 'Portuguese - Brazillanguages with full audio support'       
 'Vietnamese' 'Thailanguages with full audio support'
 'Traditional Chineselanguages with full audio support'
 'Romanianlanguages with full audio support'
 'Spanish - Spainlanguages with full audio support'
 'Simplified Chineselanguages with full audio support'
 'Koreanlanguages with full audio support'
 'Japaneselanguages with full audio support'
 'Turkishlanguages with full audio support'
 'Indonesianlanguages with full audio support'
 'Germanlanguages with full audio support' 'Hindi'
 'Malaylanguages with full audio support'
 'Polishlanguages with full audio support'
 'Englishlanguages with full audio support' 'Belarusian' 'Catalan'
 'Kazakh' 'Georgian' 'Russianlanguages with full audio support'
 'Italianlanguages with full audio support'
 'Hindilanguages with full audio support'
 'Catalanlanguages with full audio support' 'Armenian' 'Basque' 'Estonian'
 'Filipino' 'Galician' 'Hebrew' 'Malay' 'Slovak' 'Slovenian'
 'Swedishlanguages with full audio support'
 'Czechlanguages with full audio support' 'Latvian' 'Lithuanian'
 'Slovaklanguages with full audio support'
 'Serbianlanguages with full audio support' 'Serbian'
 'Portuguese - Portugallanguages with full audio support' 'Croatian'
 'Lithuanianlanguages with full audio support'
 'Frenchlanguages with full audio support'
 'Croatianlanguages with full audio support'
 'Greeklanguages with full audio support'
 'Hungarianlanguages with full audio support'
 'Hebrewlanguages with full audio support' 'Afrikaans'
 'Finnishlanguages with full audio support'
 'Dutchlanguages with full audio support'
 'Afrikaanslanguages with full audio support'
 'Traditional Chinese (text only)']

# Join the elements into a single string
combined_string = ' '.join(supported_languages)

# Split the combined string using comma as the delimiter
split_languages = combined_string.split(', ')

print(split_languages)

###########################

import pandas as pd 
df = pd.read_csv('data_clean2.csv')
input_string = df['Genres'].str.split(', ', expand=True).stack().unique()
developpeur_string = ', '.join(input_string)
print(developpeur_string)

###########################

import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient


def clean_CSV(input_text):
    # Use BeautifulSoup to parse and remove HTML tags
    soup = BeautifulSoup(input_text, 'html.parser')
    clean_text = soup.get_text()

    # Remove characters not in AZERTY keyboard layout
    clean_text = re.sub(r'[^a-zA-Z0-9\séèçàêîôû\'"\-.,;:!@#~&\[\]\(\)_+=<>?/|\\%]', '', clean_text)
    #Replace multiple white spaces by one only
    clean_text = re.sub(r'\s+', ' ', clean_text)

    return clean_text

row = ""
result = clean_CSV(row)
print(result)