from flask import Flask, render_template, request, redirect, url_for, flash
import os
import numpy as np
import cv2
# import your model loading method here
# from tensorflow import keras
# model = keras.models.load_model('path_to_your_model.h5')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you would handle the form data, e.g., send email or store in DB
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        flash('Your message has been sent!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/result', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == "POST":
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'Data', 'val', f.filename)
        f.save(filepath)

        a2 = cv2.imread(filepath)
        a2 = cv2.resize(a2, (224, 224))
        a2 = np.array(a2)
        a2 = a2 / 255.0
        a2 = np.expand_dims(a2, 0)

        # pred = model.predict(a2)
        # pred = pred.argmax()
        pred = 0  # Dummy prediction for now

        df_labels = {
            'arborio': 0,
            'basmati': 1,
            'ipsala': 2,
            'jasmine': 3,
            'karacadag': 4
        }
        for i, j in df_labels.items():
            if pred == j:
                prediction = i

    return render_template('results.html', prediction_text=prediction)

if __name__ == '__main__':
    app.run(debug=True)
