from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from file_categorizer import categorize_file
from transaction_classifier import classify_transaction
from normalize_transactions import (
    normalize_chase_credit_card,
    normalize_chase_bank,
    normalize_citi_credit_card,
    combine_transactions,
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save files

@app.route('/')
def home():
    return render_template('upload.html')  # We'll create this next

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No files uploaded!"}), 400
    
    files = request.files.getlist('file')  # Get a list of files
    all_transactions = []

    for file in files:
        if file.filename == '':
            continue  # Skip empty files
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Categorize the file
        file_category = categorize_file(filepath)
        
        # Load the file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Normalize transactions based on the file category
        if file_category == "Chase Credit Card Statement":
            normalized_df = normalize_chase_credit_card(df)
        elif file_category == "Chase Bank Statement":
            normalized_df = normalize_chase_bank(df)
        elif file_category == "Citi Credit Card Statement":
            normalized_df = normalize_citi_credit_card(df)
        else:
            return jsonify({"error": f"Unsupported file type: {file_category}"}), 400
        
        # Add normalized transactions to the list
        all_transactions.append(normalized_df)
    
    # Combine all transactions into a single DataFrame
    combined_transactions = combine_transactions(all_transactions)
    
    # Convert the DataFrame to a list of dictionaries (JSON-friendly format)
    transactions_json = combined_transactions.to_dict(orient="records")
    
    # Render the transactions in the HTML template
    return render_template('transactions.html', transactions=transactions_json)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Create uploads folder
    app.run(debug=True)
