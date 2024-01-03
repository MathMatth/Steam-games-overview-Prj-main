import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from Who_s_that_Champ.TrainRecognitionModel import create_model, make_prediction, get_local_data

app = Flask(__name__)
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img_path = file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        
        #img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 

        # charger le model
        model = tf.keras.models.load_model('/model')

        # Appeler get_local_data pour obtenir class_names
        _, _, class_names = get_local_data("/Who_s_that_Champ/Dataset champion")
        
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img = image.load_img(img_path, target_size=(240, 240))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img/255.0  # Normalisation
        prediction_result = make_prediction(model, img_path, class_names)
        # Effectuez le traitement de la prédiction et retournez le résultat à afficher
        # Créez le code HTML pour afficher l'image et la prédiction
        result_html = '<div style="display: flex; flex-direction: column; align-items: center; text-align: center;">'
        result_html += f'<img src="{url_for("uploaded_file", filename=filename)}" alt="Image soumise" >'
        result_html += f'<p>Le champion reconnu est {prediction_result}</p>'
        result_html += '<a href="/"><button>Retour</button></a>'  # Bouton "Retour" redirigeant vers la page d'accueil
        result_html += '</div>'

        return  result_html 
    else:
        return "Format de fichier non pris en charge."

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)