import os
from PIL import Image

# Function to rename and convert .jpg files to .png
def rename_jpg_to_png(folder_path, folder_name, parent_directory):
    i = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'):

            png_image = Image.open(parent_directory + "\\" + folder_name + "\\" + filename)
            jpeg_image = png_image.convert("RGB")
            jpeg_image.save(parent_directory + "\\" + folder_name + "\\" + folder_name + "_" + str(i) + ".jpg", "JPEG")
            i += 1
            os.remove(parent_directory + "\\" + folder_name + "\\" + filename)

# List of folder names
folder_names = ['Ahri', 'Annie', 'Miss_fortune', 'Jinx', 'Nidalee', 'Urgot']

# Specify the parent directory where the folders are located
parent_directory = "bloc 4 DLWho_s_that_Champn\Dataset champion"

# Iterate through each folder and rename .jpg files to .png
for folder_name in folder_names:
    folder_path = os.path.join(parent_directory, folder_name)
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        rename_jpg_to_png(folder_path, folder_name, parent_directory)
    else:
        print(f"Folder not found: {folder_path}")

