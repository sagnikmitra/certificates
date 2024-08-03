import pandas as pd
import random
import string

def generate_alphanumeric_id(length=5):
    """Generate a random alphanumeric ID of given length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_unique_ids(csv_path):
    df = pd.read_csv(csv_path)
    existing_ids = set()
    ids = []
    
    # Generate unique IDs
    for _ in range(len(df)):
        while True:
            new_id = generate_alphanumeric_id()
            if new_id not in existing_ids:
                existing_ids.add(new_id)
                ids.append(new_id.lower())
                break
    
    df['cert_id'] = ids
    df.to_csv(csv_path, index=False)

# Generate IDs for all required CSV files
generate_unique_ids("participants.csv")
generate_unique_ids("core.csv")
generate_unique_ids("evangelist.csv")
generate_unique_ids("winners.csv")
