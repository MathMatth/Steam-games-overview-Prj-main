from PIL import Image
import os

def mirror_swap_image(input_path):
    i = 0
    try:
        for filename in os.listdir(input_path):
            # Open the input image
            image = Image.open(input_path + "\\" + filename)
            
            # Convert image into RGB
            image = image.convert("RGB")

            # Mirror the image horizontally
            mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # Save the mirrored image
            mirrored_image.save(input_path + "\\" + filename[:-4] + "Mirror.jpg")

            print(f"Image mirrored and saved to {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # List of folder names
    #folder_names = ['Ahri', 'Annie', 'Corki', 'Garen', 'Miss_fortune', 'Jinx', 'Nidalee', 'Poppy', 'Yasuo', 'Urgot']
    folder_names = ['Corki', 'Garen', 'Miss_fortune', 'Jinx', 'Nidalee', 'Poppy', 'Yasuo']

    # Specify the parent directory where the folders are located
    parent_directory = "bloc 4 DL\Who_s_that_Champ\Dataset champion"

    for folder_name in folder_names:
        folder_path = os.path.join(parent_directory, folder_name)
        
        # Check if the folder exists
        if os.path.exists(folder_path):
            mirror_swap_image(folder_path)
        else:
            print(f"Folder not found: {folder_path}")