from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Path to the directory where files will be stored
PERSISTENT_STORAGE_PATH = '/home/ghost/app/persistent_storage/'
container_2_url = (os.getenv('CONTAINER_2_URI') or 'http://localhost:4000') + '/calculate-sum'

if not os.path.exists(PERSISTENT_STORAGE_PATH):
    print("ERROR PERSISTENT_STORAGE_PATH not found")
    os.makedirs(PERSISTENT_STORAGE_PATH)

def save_file(filename, data):
    try:
        filepath = os.path.join(PERSISTENT_STORAGE_PATH, filename)
        with open(filepath, 'w') as file:
            file.write(data)
        return True, "Success."
    except Exception as e:
        return False, f"Error while storing the file to the rtorage: {str(e)}"

def file_exists(filename):
    return os.path.exists(os.path.join(PERSISTENT_STORAGE_PATH, filename))

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        request_data = request.get_json()
        filename = request_data.get('file')
        data = request_data.get('data')
        
        if not filename or not data:
            return jsonify({"file": filename, "error": "Invalid JSON input."}), 400
        
        success, message = save_file(filename, data)
        
        if success:
            return jsonify({"file": filename, "message": message}), 200
        else:
            return jsonify({"file": filename, "error": message}), 500
    
    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        request_data = request.get_json()
        filename = request_data.get('file')
        product = request_data.get('product')
        
        if not filename or not product:
            return jsonify({"file": filename, "error": "Invalid JSON input."}), 400
        
        if not file_exists(filename):
            return jsonify({"file": filename, "error": "File not found."}), 404
        
        # Communicate with container 2 to calculate the product sum
        # Assuming container 2 is accessible via HTTP request and has an endpoint /calculate-sum
        response = requests.post(container_2_url, json={"file": filename, "product": product})

        return response.json()
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({"file": filename, "error": "Error while calculating the sum." }), 500
    
    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

