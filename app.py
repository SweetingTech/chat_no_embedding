from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
import json
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    uploaded_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
                     if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))
                     and f.endswith('.txt')]
    return render_template('index.html', uploaded_files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
    return redirect(url_for('index'))

@app.route('/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
             if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))
             and f.endswith('.txt')]
    return jsonify({'files': files})

def extract_document_name(message):
    # Look for @filename.txt pattern
    matches = re.findall(r'@([\w.-]+\.txt)', message)
    if matches:
        return matches[0]
    return None

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    ip_address = data.get('ip_address', 'localhost')
    port = data.get('port', '1234')
    
    # Debug print
    print(f"\nReceived user input: {user_input}")
    
    document_name = extract_document_name(user_input)
    document_content = ''
    
    if document_name:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], document_name)
        print(f"Looking for file at: {filepath}")  # Debug print
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                document_content = file.read()
            print(f"File content read: {document_content}")  # Debug print
            
            # Clean up the user input by removing the @mention
            clean_input = user_input.replace(f'@{document_name}', f'the file {document_name}')
            prompt = f"""I have a file named '{document_name}' with the following content:

BEGIN FILE CONTENT
{document_content}
END FILE CONTENT

{clean_input}"""
        else:
            print(f"File not found at: {filepath}")  # Debug print
            return jsonify({'response': f"The document '{document_name}' was not found in the uploads folder."})
    else:
        prompt = user_input
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. When analyzing file contents, work directly with the content provided between BEGIN FILE CONTENT and END FILE CONTENT markers."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    print("\nSending messages to LM Studio:")
    print(json.dumps(messages, indent=2))

    lm_studio_url = f"http://{ip_address}:{port}/v1/chat/completions"

    try:
        # Get model info
        model_info_response = requests.get(f"http://{ip_address}:{port}/v1/models")
        if model_info_response.status_code != 200:
            return jsonify({'response': 'Error: Unable to get model information from LM Studio'})
        
        model_info = model_info_response.json()
        if not model_info.get('data'):
            return jsonify({'response': 'Error: No models available in LM Studio'})
        
        model_id = model_info['data'][0]['id']
        
        # Make the chat completion request
        response = requests.post(
            lm_studio_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "model": model_id,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False
            }),
            timeout=30
        )

        print("\nLM Studio Response Status Code:", response.status_code)
        print("LM Studio Response Content:", response.content.decode())

        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content'].strip()
            if not response_text:
                response_text = "Received empty response from LM Studio"
        else:
            response_text = f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LM Studio: {str(e)}")
        response_text = f"Error connecting to LM Studio: {str(e)}"

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)