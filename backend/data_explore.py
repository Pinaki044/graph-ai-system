import pandas as pd
import os

data_path = "data"

for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".jsonl"):
            full_path = os.path.join(root, file)
            
            print(f"\n📂 File: {file}")
            print(f"Path: {full_path}")
            
            # Read JSONL
            df = pd.read_json(full_path, lines=True)
            
            print("Columns:")
            for col in df.columns:
                print(" -", col)
            
            print("\nSample Data:")
            print(df.head(2))
            
            break   # only read 1 file per folder (important)