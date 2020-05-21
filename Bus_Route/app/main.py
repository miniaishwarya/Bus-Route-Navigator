# Main execution point

# Inputs: Filename, destination 
# Output: A list or a string

import cv2 as cv

from app import route_mapping as rm

def routemapp(image_filename, dest, loc):

    filename= '\\' + image_filename

    # This is the path where all the uploaded images of the bus board are stored. Edit this line. 
    path = r'C:\Users\Mini Aishwarya\Documents\Project\Web-app\Bus_Route\app\static\images\uploads'
    path = path + filename

    print('Image path', path)

    result=[]

    result = rm.mainFindRoute(path, dest,loc)

    if(type(result)!='<class \'NoneType\'>'):
        if len(result) == 1:
            print(result)
            print('error string')
        else:
            print(result)
            pass
    else:
        pass

    return result

