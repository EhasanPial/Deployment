from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
import os
from tensorflow.keras.preprocessing import image


TEMPLATE_DIR = os.path.abspath('../templates')
STATIC_DIR = os.path.abspath('../static')

app = Flask(__name__)


model = load_model('my_model_1.h5')
target_img = os.path.join(os.getcwd() , 'static/images')


@app.route('/')
def index_view():
    return render_template('index.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/read_details')
def read_details():
    return render_template('read_details.html')
@app.route('/fundus_check')
def fundus():
    return render_template('fundus_check.html')
#Allow files with extension png, jpg and jpeg
ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT
           
# Function to load and prepare the image in right shape
def read_image(filename):
    img = load_img(filename, target_size=(224,224,3))
    #img = img.reshape(1,224,224,3)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    #x = preprocess_input(x)
    return x

@app.route('/fundus_check',methods=['GET','POST'])
def fundus_check():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename): #Checking file format
            filename = file.filename
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            img = read_image(file_path) #prepressing method
            class_prediction=model.predict(img) 
            classes_x=np.argmax(class_prediction,axis=1)
            if classes_x == 0:
                retina = "Normal"
            elif classes_x == 1:
                retina = "Cataract"
            elif classes_x == 2:
                retina = "Glaucoma"
            elif classes_x == 3:
                retina = "Retina Disease"
            #'retina' , 'prob' . 'user_image' these names we have seen in predict.html.
            return render_template('predict.html', retina = retina,prob=class_prediction, user_image = file_path)
        else:
            return "Unable to read the file. Please check file extension"


@app.route('/predict',methods=['GET','POST'])
def predict_check():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename): #Checking file format
            filename = file.filename
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            img = read_image(file_path) #prepressing method
            class_prediction=model.predict(img) 
            classes_x=np.argmax(class_prediction,axis=1)
            if classes_x == 0:
                retina = "Normal"
            elif classes_x == 1:
                retina = "Cataract"
            elif classes_x == 2:
                retina = "Glaucoma"
            elif classes_x == 3:
                retina = "Retina Disease"
            #'retina' , 'prob' . 'user_image' these names we have seen in predict.html.
            
            return render_template('predict.html', retina = retina,prob=class_prediction, user_image = file_path)
        else:
            return "Unable to read the file. Please check file extension"


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False, port=8000)