from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save files

@app.route('/')
def home():
    return render_template('upload.html')  # We'll create this next

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded!"
    file = request.files['file']
    if file.filename == '':
        return "No file selected!"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "File uploaded!"

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Create uploads folder
    app.run(debug=True)