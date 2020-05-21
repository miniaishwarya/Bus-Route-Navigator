import cv2
import numpy as np

#import import_ipynb#for enabling importing of ipynb

from app import matching_test2 as m_t #ipynb for matching
from app import pre_processing as pre_p#ipynb for pre processing

from googletrans import Translator

import matplotlib.pyplot as plt#for plotting image

from pytesseract import image_to_string
import pytesseract

def testing(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract'

    input1 = cv2.imread(path)

    gray = pre_p.get_grayscale(input1)
    erosion = pre_p.erode(gray)
    dilation = pre_p.dilate(erosion)

    #for printing gray image
    #plt.imshow(gray)
    #plt.show()

    output = pytesseract.image_to_string(gray, lang='mal')
    #print("\nOutput obtained by tesseract from image:-\n")
    #print(output)
    #output is of type string

    array = output.split() #split() returns a list form of "output", array is a list with each element as a malayalam word

    #\u200d is a non printable character used in languages(Read wiki)

    #print("\nThe malayalam word array :-\n")
    #print(array)

    #Declaring object "trans_1" for accessing Google translator API
    trans_1 = Translator()
    text_eng = trans_1.translate(array) #Function for translating the malayalam words in array
    #text_eng is an object with attributes

    #print("\nThe English translated word :-\n")
    list_eng = []

    for x in text_eng:
        list_eng.append(x.text)
        
    #print(list_eng)
        
    #print("\nEnglish words after matching:-\n")
    list_eng = m_t.matching(list_eng)

    #m_t.cleaning()

    # prints the entire words matched, route number and the route
    #print(list_eng)

    result=[]

    result.append(list_eng[0])
    result.append(list_eng[1]-1)

    # prints words matched and route number
    #print(result)

    print('Result in testing_current.py', result)
    return result  
# ".text" is an attribute of the object text_eng, which has the translated word     
     