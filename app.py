from flask import Flask, request, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

def identify_plant(image_path, api_key):
    url = "https://api.plant.id/v2/identify"
    headers = {"Api-Key": api_key}
    
    with open(image_path, "rb") as image_file:
        files = {"images": image_file}
        data = {"organs": ["leaf"]}

        response = requests.post(url, headers=headers, files=files, data={"data": json.dumps(data)})
    
    if response.status_code == 200:
        try:
            result = response.json()
            if "suggestions" in result and len(result["suggestions"]) > 0:
                first_suggestion = result["suggestions"][0]
                scientific_name = first_suggestion["plant_details"].get("scientific_name", "Unknown")
                common_name = first_suggestion.get("plant_name", "Unknown")
                probability = first_suggestion.get("probability", "Unknown")
                return {
                    "common_name": common_name,
                    "scientific_name": scientific_name,
                    "probability": f"{probability:.2%}"
                }
            else:
                return {"error": "No suggestions found."}
        except (ValueError, KeyError, IndexError) as e:
            return {"error": f"Error parsing JSON response: {str(e)}"}
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        
        if file:
            # Save the uploaded file
            image_path = os.path.join("uploads", file.filename)
            file.save(image_path)

            # Call the plant identification function
            api_key = "Your actual API key"
            result = identify_plant(image_path, api_key)
            return jsonify(result)
    
    return render_template('index.html')

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    app.run(debug=True)
