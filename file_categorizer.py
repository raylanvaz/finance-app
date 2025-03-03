import pandas as pd

# Define weights for each criterion
WEIGHTS = {
    "file_name": 0.15,  # Weight for file name
    "column_headers": 0.75,  # Weight for column headers
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

# Define expected columns for Citi Credit Card Statements
EXPECTED_COLUMNS_CITI_CC = [
    "Status", "Date", "Description", "Debit", "Credit"
]

def score_file_name(file_name):
    """Score the file name based on keywords."""
    keywords_chase_cc = ["chase"]  # Keywords for credit card statements
    keywords_chase_bank = ["chase"]  # Keywords for bank statements
    keywords_citi_cc = ["Date Range"]  # Keywords for Citi credit card statements
    
    score_chase_cc = sum(1 for keyword in keywords_chase_cc if keyword in file_name.lower())
    score_chase_bank = sum(1 for keyword in keywords_chase_bank if keyword in file_name.lower())
    score_citi_cc = sum(1 for keyword in keywords_citi_cc if keyword in file_name.lower())
    
    # Normalize scores to [0, 1]
    return {
        "chase_credit_card": score_chase_cc / len(keywords_chase_cc),
        "chase_bank": score_chase_bank / len(keywords_chase_bank),
        "citi_credit_card": score_citi_cc / len(keywords_citi_cc)
    }

def score_column_headers(headers):
    """Score the column headers based on expected columns."""
    matches_chase_cc = sum(1 for header in headers if header in EXPECTED_COLUMNS_CHASE_CC)
    matches_chase_bank = sum(1 for header in headers if header in EXPECTED_COLUMNS_CHASE_BANK)
    matches_citi_cc = sum(1 for header in headers if header in EXPECTED_COLUMNS_CITI_CC)
    
    # Normalize scores to [0, 1]
    return {
        "chase_credit_card": matches_chase_cc / len(EXPECTED_COLUMNS_CHASE_CC),
        "chase_bank": matches_chase_bank / len(EXPECTED_COLUMNS_CHASE_BANK),
        "citi_credit_card": matches_citi_cc / len(EXPECTED_COLUMNS_CITI_CC)
    }

def score_file_extension(file_name):
    """Score the file extension."""
    return 1 if file_name.lower().endswith(".csv") else 0

def determine_file_type(total_score_chase_cc, total_score_chase_bank, total_score_citi_cc):
    # Create a dictionary to map scores to their corresponding file types
    scores_and_types = {
        "Chase Credit Card Statement": total_score_chase_cc,
        "Chase Bank Statement": total_score_chase_bank,
        "Citi Credit Card Statement": total_score_citi_cc,
    }

    # Find the file type with the highest score
    winning_type = max(scores_and_types, key=scores_and_types.get)
    winning_score = scores_and_types[winning_type]

    # Determine the final file type based on the winning score
    if winning_score >= 0.8:
        return winning_type
    else:
        return "Generic CSV"

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
        scores["file_name"]["chase_credit_card"] * WEIGHTS["file_name"] +
        scores["column_headers"]["chase_credit_card"] * WEIGHTS["column_headers"] +
        scores["file_extension"] * WEIGHTS["file_extension"]
    )
    
    total_score_chase_bank = (
        scores["file_name"]["chase_bank"] * WEIGHTS["file_name"] +
        scores["column_headers"]["chase_bank"] * WEIGHTS["column_headers"] +
        scores["file_extension"] * WEIGHTS["file_extension"]
    )

    total_score_citi_cc = (
        scores["file_name"]["citi_credit_card"] * WEIGHTS["file_name"] +
        scores["column_headers"]["citi_credit_card"] * WEIGHTS["column_headers"] +
        scores["file_extension"] * WEIGHTS["file_extension"]
    )
    
    file_type = determine_file_type(total_score_chase_cc, total_score_chase_bank, total_score_citi_cc)
    
    # Determine file type based on the highest score
    return file_type