from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Azure OpenAI settings
AZURE_API_KEY = "ced843df306045f0879937317b0914a7"
AZURE_ENDPOINT = "https://similarity-instance-lexys.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-35-turbo"

def get_similarity(word1, word2):
    # Define the prompt for the model
    prompt = f"Rate the similarity between the words '{word1}' and '{word2}' on a scale from 0 to 1."

    # Set up the headers
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    # Define the request body
    data = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.5
    }

    # Construct the API URL
    api_url = f"{AZURE_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/completions?api-version=2023-07-01-preview"

    # Make the API request
    response = requests.post(api_url, headers=headers, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        result = response.json()
        similarity_score = result['choices'][0]['text'].strip()
        return similarity_score
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/api/similarity', methods=['POST'])
def similarity():
    data = request.get_json()
    word1 = data.get('word1')
    word2 = data.get('word2')

    if not word1 or not word2:
        return jsonify({"error": "Please provide both word1 and word2."}), 400

    similarity_score = get_similarity(word1, word2)
    return jsonify({"similarity_score": similarity_score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
