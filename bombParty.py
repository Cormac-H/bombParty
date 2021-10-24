import time
import keyboard
import pyperclip
import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageGrab



def main():
    start_time = time.time()
    dictionary = open('dict.txt', 'r')
    temp = dictionary.read().splitlines()
    words = {}

    for line in temp:

        # Read each word to hash table
        words[line] = False

        # Break on file end
        if not line:
            break
    
    while True:
        # Take Screenshot        
        image = ImageGrab.grab(bbox = (765,540,855,600))  # Parameters will change per screen size and chat position
        image = np.asarray(image)


        # Pre-process image and print text

        retval, img = cv2.threshold(image,200,255, cv2.THRESH_BINARY)
        img = cv2.resize(img,(0,0),fx=3,fy=3)

        kernel_erosion = np.ones((3,3), np.uint8)
        img = cv2.erode(img, kernel_erosion, iterations=1)

        #img = cv2.GaussianBlur(img,(11,11),0)
        #img = cv2.medianBlur(img,9)

        # Save Image
        image = Image.fromarray(img)
        image.save("screenshot.png")

        # Extract text from image
        pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(img, lang='bombPartyLang', config='--psm 7')

        text = text.split("\n")[0].upper()

        # Find first match in hashmap and mark is as used

        for key, value in words.items():
            if not value and (text in key):
                # Copy text to clipboard and print results
                pyperclip.copy(key)

                print(text)
                print(key + "\n")

                words[key] = True
                break

        # Enter to run script    
        keyboard.wait("enter")


    print("--- %s seconds ---" % (time.time() - start_time)) 


if __name__ == "__main__":
    
    main()