from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save files

@app.route('/')
def home():
    return render_template('upload.html')  # We'll create this next

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No files uploaded!"
    
    files = request.files.getlist('file')  # Get a list of files
    all_transactions = []

    for file in files:
        if file.filename == '':
            continue  # Skip empty files
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Read and classify transactions
        df = pd.read_csv(filepath)
        transactions = df.to_dict("records")
        # for transaction in transactions:
        #     transaction['Category'] = classify_transaction(transaction['Description'])
        # all_transactions.extend(transactions)  # Combine all transactions
    
    return str(transactions)  # Show all transactions from all files

# Define your categories and keywords
CATEGORIES = {
    "Groceries": ["walmart", "kroger", "aldi"],
    "Entertainment": ["netflix", "spotify"],
    "Utilities": ["electric", "water co"]
}

def classify_transaction(description):
    description_lower = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return "Other"

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Create uploads folder
    app.run(debug=True)
