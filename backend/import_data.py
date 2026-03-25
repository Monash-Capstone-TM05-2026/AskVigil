import pandas as pd
from main import load_model, save_to_db # Reuse your existing logic

def run_import(file_path: str, category: str):
    # 1. Load the data
    print(f"Reading {file_path}...")
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # 2. Extract the text column (assuming your column is named 'text')
    # Clean out empty rows or non-string data
    content_list = df['text'].dropna().astype(str).tolist()
    
    # 3. Process in batches to save memory (Important for Oracle Free Tier)
    batch_size = 100
    for i in range(0, len(content_list), batch_size):
        batch = content_list[i : i + batch_size]
        print(f"Processing batch {i//batch_size + 1} ({len(batch)} rows)...")
        save_to_db(batch, category)
        
    print("✅ Import Complete!")

if __name__ == "__main__":
    # Example: python import_data.py my_dataset.csv "Manglish-Corpus"
    import sys
    run_import(sys.argv[1], sys.argv[2])