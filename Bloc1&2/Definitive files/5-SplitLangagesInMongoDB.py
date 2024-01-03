from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://hydronalpha:hydronalpha@cluster0.u4etida.mongodb.net/')
db = client['SteamDBClean']  # Replace with your database name
collection = db['SteamInfosGames2']  # Replace with your collection name

supported_languages = ['Czech', 'Danish', 'Dutch', 'English', 'Finnish', 'French', 'German', 'Hungarian', 'Italian', 'Japanese', 'Korean', 'Norwegian', 'Polish', 'Portuguese - Portugal', 'Portuguese - Brazil', 'Romanian', 'Russian', 'Simplified Chinese', 'Spanish - Spain', 'Swedish', 'Thai', 'Traditional Chinese', 'Turkish', 'Bulgarian', 'Ukrainian', 'Greek', 'Spanish - Latin America', 'Vietnameselanguages with full audio support', 'Arabiclanguages with full audio support', 'Arabic', 'Ukrainianlanguages with full audio support', 'Spanish - Latin Americalanguages with full audio support', 'Indonesian', 'Persian', 'Portuguese - Brazillanguages with full audio support', 'Vietnamese', 'Thailanguages with full audio support', 'Traditional Chineselanguages with full audio support', 'Romanianlanguages with full audio support', 'Spanish - Spainlanguages with full audio support', 'Simplified Chineselanguages with full audio support', 'Koreanlanguages with full audio support', 
                       'Japaneselanguages with full audio support', 'Turkishlanguages with full audio support', 'Indonesianlanguages with full audio support', 'Germanlanguages with full audio support', 'Hindi', 'Malaylanguages with full audio support', 'Polishlanguages with full audio support', 'Englishlanguages with full audio support', 'Belarusian', 'Catalan', 'Kazakh', 'Georgian', 'Russianlanguages with full audio support', 'Italianlanguages with full audio support', 'Hindilanguages with full audio support', 'Catalanlanguages with full audio support', 'Armenian', 'Basque', 'Estonian', 'Filipino', 'Galician', 'Hebrew', 'Malay', 'Slovak', 'Slovenian', 'Swedishlanguages with full audio support', 'Czechlanguages with full audio support', 'Latvian', 'Lithuanian', 'Slovaklanguages with full audio support', 'Serbianlanguages with full audio support', 'Serbian', 'Portuguese - Portugallanguages with full audio support', 'Croatian', 'Lithuanianlanguages with full audio support', 'Frenchlanguages with full audio support', 'Croatianlanguages with full audio support', 'Greeklanguages with full audio support', 'Hungarianlanguages with full audio support', 'Hebrewlanguages with full audio support', 'Afrikaans', 'Finnishlanguages with full audio support', 'Dutchlanguages with full audio support', 
                       'Afrikaanslanguages with full audio support', 'Traditional Chinese (text only)']


# Update documents
for document in collection.find():
    supported_languages_present = document.get("Langages supportés", [])
    for language in supported_languages:
        if language in supported_languages_present:
            collection.update_one(
                {"_id": document["_id"]},
                {"$set": {language: True}}
            )

# Delete the "Langages supportés" field from all documents
collection.update_many({}, {"$unset": {"Langages supportés": ""}})

# Close the connection
client.close()