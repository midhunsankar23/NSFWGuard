from flask import Flask, request, jsonify, render_template
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the saved model
model = load_model('nude_safe_classifier.h5')
img_size = (299, 299)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Check if the file has an allowed extension if needed
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension'}), 400

    try:
        # Prepare the image for prediction
        img = Image.open(file.stream)
        img = img.resize(img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image

        # Make predictions
        predictions = model.predict(img_array)

        # Convert predictions to binary labels (0 or 1)
        binary_prediction = int(np.round(predictions[0]))

        result = {'prediction': binary_prediction}
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
