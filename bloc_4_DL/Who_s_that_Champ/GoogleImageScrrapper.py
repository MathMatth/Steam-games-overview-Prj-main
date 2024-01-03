import os
import time
import string
import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to create the "images" folder if it doesn't exist
def create_images_folder():
    if not os.path.exists("images"):
        os.makedirs("images")

# Function to sanitize a string to be used as a file name
def clean_filename(filename):
    # Remove characters that are not valid in file names
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c if c in valid_chars else '_' for c in filename)
    return cleaned_filename

# Function to fetch and download images with class="rg_i Q4LuWd" and retrieve their direct URLs from the preview
def fetch_and_download_images(url, champion_name, image_type):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed

    #Create a counter of images treated
    Image_treated_count = 0

    try:
        # Open the webpage
        driver.get(url)
        time.sleep(2)  # Wait for the page to load (you can adjust the wait time)

        # Find and click the "Tout refuser" button based on aria-label
        tout_refuser_button = driver.find_element(By.XPATH, "//button[@aria-label='Tout refuser']")
        tout_refuser_button.click()
        time.sleep(2)  # Wait for the action to take effect (you can adjust the wait time)

        # Disable safesearch to avoid blurred effect on some images
        driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[1]/div/div[2]/div/span/g-popup/div[1]/div/g-dropdown-button/g-dropdown-menu-button-caption/span/div/span[1]').click()
        driver.find_element(By.XPATH, '//*[@id="lb"]/div/g-menu/g-menu-item[3]/div/a').click()
        time.sleep(2)

        # Scroll down to the end of the page using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Find and click each image with class="rg_i Q4LuWd"
        img_elements = driver.find_elements(By.XPATH, "//img[contains(@class,'rg_i') and contains(@class,'Q4LuWd')]")
        print("Images scannées :" + str(len(img_elements)))
        img_elements = img_elements[:250]
        for img_element in img_elements:
            try :
                img_element.click()
            except :
                continue
            time.sleep(2)  # Wait for the preview to appear (you can adjust the wait time)

            # Find the preview element using the provided XPath
            try :
                preview_element = driver.find_element(By.XPATH, "//*[@id='Sva75c']/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]")
            except :
               preview_element = driver.find_element(By.XPATH, "//*[@id='Sva75c']/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[2]/div/a/img[1]")
                                                             
            # Retrieve the direct URL from the preview element
            img_url = preview_element.get_attribute("src")
            if img_url and img_url.startswith("http") :
                img_url = urljoin(url, img_url)  # Make sure the URL is absolute
                img_name = os.path.basename(img_url)

                champion_name_for_filename = champion_name.replace("+", "_")
                img_path = os.path.join("bloc 4 DL\Who_s_that_Champ\Dataset champion\\" + champion_name_for_filename, champion_name_for_filename + "_" + image_type + "_" + str(Image_treated_count) + ".jpg")  


                # Download the image using the direct URL
                try :
                    response = requests.get(img_url)
                except :
                    continue 

                if response.status_code == 200:
                    with open(img_path, "wb") as img_file:
                        img_file.write(response.content)
                        print(f"Downloaded: {img_name}")
                else:
                    print(f"Failed to download: {img_name}")

            # Find and click the close button using the class attribute
            close_buttons = driver.find_elements(By.XPATH, "//div[@class='envSYb xbf3tb']")
            if len(close_buttons) >= 3:
                close_buttons[1].click()
            else :
                close_buttons[0].click()
            
            time.sleep(2)  # Wait for the preview to close (you can adjust the wait time)
            Image_treated_count += 1

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    name_list = ['Ahri', 'Miss+fortune', "Jinx", 'Urgot']
    base_url = "https://www.google.com/search?q="
    suffix_url = "&tbm=isch#imgrc=kuW-XrOVmYAHrM"
    chibiType = "chibi"
    fanartType = "fanart"
    portraitType = "portrait"
    noType = ""

    for champion_name in name_list :
        queries = {}
        queries[base_url + "PNG+" + champion_name + " LoL" + suffix_url] = noType
        queries[base_url + champion_name + "+" + fanartType + "+LoL" + suffix_url] = fanartType
        queries[base_url + champion_name + "+" + portraitType + "+LoL" + suffix_url] = portraitType
        queries[base_url + champion_name + "+" + chibiType + "+LoL" + suffix_url] = chibiType

        for query in queries.keys() :
            fetch_and_download_images(query, champion_name, queries[query])
    
