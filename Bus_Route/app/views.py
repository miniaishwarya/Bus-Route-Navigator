from app import app
from app import main
from app import routes
from app import destination_matching

from flask import render_template, request, redirect, flash, url_for, make_response, jsonify, abort, session

from werkzeug.utils import secure_filename

from PIL import Image

import os


result=[]

global dest
dest=""

def reset_route():
    global result
    result=[]
    del result[:]
    return result

@app.route('/')
def test():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Form Upload 
@app.route('/findroute', methods=['POST', 'GET'])
def upload():
    
    error=''

    if request.method == 'POST':
    
        global dest
        input_dest = ""
        input_dest = request.form["destination"]
        loc=""

        dest = destination_matching.destination_validation(input_dest)

        if request.files:
            image = request.files['image']
            if image.filename == "":
                flash('Image must have a filename','error')
                return redirect(request.url)

            if not allowed_image(image.filename):
                flash("That image extension is not allowed.",'error')
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))             

                global result
                result=[]
    
                result = reset_route()

                result = routemapping(filename,dest, loc)

                print('Result from route mapping', result)

                result = routes.orgRoute(result)              

                if 'Error' in result[0]:
                    result='Error'
                    return redirect(url_for('routenogo', result=result))
                else:
                    return render_template('go.html', result=result)

        return redirect(url_for('upload'))
    else:
        pass
        
    return render_template('upload.html')

# Text detection and mapping the route
def routemapping(filename, dest, loc):

    loc=""
    
    result = main.routemapp(filename, dest, loc)

    return result



@app.route('/findroute/nogo')
def routenogo():
    session.clear()
    return render_template('nogo.html')

# Allows to follow image extensions
def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False  


@app.route('/findroute/displayroutes')
def displayroute():
    session.clear()
    return render_template('displayroutes.html', result=result, dest=dest)



@app.route('/findroute/go')
def routego():
    return render_template('go.html')
 
    

