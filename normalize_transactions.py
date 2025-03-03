import pandas as pd

def normalize_chase_credit_card(df):
    """
    Normalize transactions from a Chase Credit Card statement.
    Columns in the input DataFrame should match EXPECTED_COLUMNS_CHASE_CC.
    """
    normalized_df = pd.DataFrame()
    normalized_df["date"] = df["Post Date"]
    normalized_df["description"] = df["Description"]
    normalized_df["amount"] = df["Amount"]
    normalized_df["category"] = df["Category"]
    normalized_df["source"] = "chase_credit_card"
    return normalized_df

def normalize_chase_bank(df):
    """
    Normalize transactions from a Chase Bank statement.
    Columns in the input DataFrame should match EXPECTED_COLUMNS_CHASE_BANK.
    """
    normalized_df = pd.DataFrame()
    normalized_df["date"] = df["Posting Date"]
    normalized_df["description"] = df["Description"]
    normalized_df["amount"] = df["Amount"]
    normalized_df["category"] = ""  # No category information in Chase Bank statements
    normalized_df["source"] = "chase_bank"
    return normalized_df

def normalize_citi_credit_card(df):
    """
    Normalize transactions from a Citi Credit Card statement.
    Columns in the input DataFrame should match EXPECTED_COLUMNS_CITI_CC.
    """
    normalized_df = pd.DataFrame()
    normalized_df["date"] = df["Date"]
    normalized_df["description"] = df["Description"]
    normalized_df["amount"] = df["Debit"].fillna(0) - df["Credit"].fillna(0)  # Calculate net amount
    normalized_df["category"] = ""  # No category information in Chase Bank statements
    normalized_df["source"] = "citi_credit_card"
    return normalized_df

def remove_duplicates(df):
    """
    Remove duplicate transactions based on date, description, and amount.
    """
    return df.drop_duplicates(subset=["date", "description", "amount"])

def combine_transactions(transactions_list):
    """
    Combine multiple normalized DataFrames into one and remove duplicates.
    """
    combined_df = pd.concat(transactions_list, ignore_index=True)
    combined_df = remove_duplicates(combined_df)
    return combined_df