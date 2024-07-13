import csv
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Directory where files will be stored
STORAGE_DIR = '/persistent_storage'

# Ensure the storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@app.route('/')
def home():
    return "Welcome to Microservice 1"

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()
    file_name = data.get('file')
    file_data = data.get('data')

    if not file_name or not file_data:
        return jsonify({"file": file_name, "error": "Invalid JSON input."}), 400

    try:
        file_path = os.path.join(STORAGE_DIR, file_name)
        with open(file_path, 'w') as f:
            f.write(file_data)

        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    file_name = data.get('file')
    product = data.get('product')

    # Check if file name is provided
    if not file_name or not product:
        return jsonify({"file": file_name, "error": "Invalid JSON input."}), 400

    try:
        # Call Microservice 2's /calculate endpoint
        response = call_microservice2_calculate(file_name, product)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def call_microservice2_calculate(file_name, product):
    microservice2_url = 'http://microservice2.default.svc.cluster.local/calculate'
    payload = {
        "file": file_name,
        "product": product
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(microservice2_url, json=payload, headers=headers)
    return response

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)
