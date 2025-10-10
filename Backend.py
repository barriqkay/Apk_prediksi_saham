from flask import Flask, jsonify, request
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Load model
MODEL_PATH = "stock.model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/')
def home():
    return jsonify({"status": "API is running", "model": MODEL_PATH})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = np.array(data['input']).reshape(1, -1, 1)
    prediction = model.predict(input_data)
    return jsonify({"prediction": float(prediction[0][0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
