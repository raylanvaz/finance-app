import pandas as pd

# Define weights for each criterion
WEIGHTS = {
    "file_name": 0.4,  # Weight for file name
    "column_headers": 0.5,  # Weight for column headers
    "file_extension": 0.1,  # Weight for file extension
}

# Define expected columns for Chase Credit Card Statements
EXPECTED_COLUMNS_CHASE_CC = [
    "Transaction Date", "Post Date", "Description",
    "Category", "Type", "Amount", "Memo"
]

# Define expected columns for Chase Bank Statements
EXPECTED_COLUMNS_CHASE_BANK = [
    "Details", "Posting Date", "Description", "Amount", "Type","Balance","Check or Slip #"
]

def score_file_name(file_name):
    """Score the file name based on keywords."""
    keywords_chase_cc = ["chase"]  # Keywords for credit card statements
    keywords_chase_bank = ["chase"]  # Keywords for bank statements
    
    score_chase_cc = sum(1 for keyword in keywords_chase_cc if keyword in file_name.lower())
    score_chase_bank = sum(1 for keyword in keywords_chase_bank if keyword in file_name.lower())
    
    # Normalize scores to [0, 1]
    return {
        "credit_card": score_chase_cc / len(keywords_chase_cc),
        "bank": score_chase_bank / len(keywords_chase_bank),
    }

def score_column_headers(headers):
    """Score the column headers based on expected columns."""
    matches_chase_cc = sum(1 for header in headers if header in EXPECTED_COLUMNS_CHASE_CC)
    matches_chase_bank = sum(1 for header in headers if header in EXPECTED_COLUMNS_CHASE_BANK)
    
    # Normalize scores to [0, 1]
    return {
        "credit_card": matches_chase_cc / len(EXPECTED_COLUMNS_CHASE_CC),
        "bank": matches_chase_bank / len(EXPECTED_COLUMNS_CHASE_BANK),
    }

def score_file_extension(file_name):
    """Score the file extension."""
    return 1 if file_name.lower().endswith(".csv") else 0

def categorize_file(file_path):
    """Categorize the file using a weighted scoring mechanism."""
    file_name = file_path.split("/")[-1]  # Extract file name from path

    # Calculate scores for each criterion
    scores = {
        "file_name": score_file_name(file_name),
        "column_headers": score_column_headers(pd.read_csv(file_path, nrows=0).columns),
        "file_extension": score_file_extension(file_name),
    }

    # Calculate weighted average scores for each type
    total_score_chase_cc = (
        scores["file_name"]["credit_card"] * WEIGHTS["file_name"] +
        scores["column_headers"]["credit_card"] * WEIGHTS["column_headers"] +
        scores["file_extension"] * WEIGHTS["file_extension"]
    )
    
    total_score_chase_bank = (
        scores["file_name"]["bank"] * WEIGHTS["file_name"] +
        scores["column_headers"]["bank"] * WEIGHTS["column_headers"] +
        scores["file_extension"] * WEIGHTS["file_extension"]
    )

    # Determine file type based on the highest score
    if total_score_chase_cc >= 0.8 and total_score_chase_cc > total_score_chase_bank:
        return "Chase Credit Card Statement"
    elif total_score_chase_bank >= 0.8 and total_score_chase_bank > total_score_chase_cc:
        return "Chase Bank Statement"
    elif total_score_chase_cc >= 0.5 or total_score_chase_bank >= 0.5:
        return "Generic Bank Statement"
    else:
        return "Unknown File Type"