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
