import os
import argparse
import pandas as pd
import hashlib
from typing import List, Dict

def get_csv_files(directory: str) -> List[str]:
    """Recursively get all CSV files in the given directory."""
    csv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def extract_schema(df: pd.DataFrame) -> Dict[str, str]:
    """Extract schema from pandas DataFrame."""
    schema = {}
    for column in df.columns:
        dtype = str(df[column].dtype)
        if dtype == 'object':
            schema[column] = 'STRING'
        elif dtype.startswith('int'):
            schema[column] = 'INTEGER'
        elif dtype.startswith('float'):
            schema[column] = 'FLOAT'
        elif dtype == 'bool':
            schema[column] = 'BOOLEAN'
        elif dtype.startswith('datetime'):
            schema[column] = 'TIMESTAMP'
        else:
            schema[column] = 'STRING'  # Default to STRING for unknown types
    return schema

def generate_schema_text(schema: Dict[str, str], csv_file: str, df: pd.DataFrame, include_rows_num: int) -> str:
    """Generate schema text from the schema dictionary and include the CSV file name and sample data."""
    schema_lines = [f"CSV File: {csv_file}\n"]
    schema_lines.extend([f"{field}: {dtype}" for field, dtype in schema.items()])
    
    if include_rows_num > 0:
        schema_lines.append(f"\nSample Data (first {include_rows_num} rows):")
        sample_data = df.head(include_rows_num).to_string(index=False)
        schema_lines.append(sample_data)
    
    return "\n".join(schema_lines)

def save_schema(schema_text: str, csv_file: str, output_dir: str) -> None:
    """Save schema text to a file in the output directory."""
    # Generate MD5 hash of the schema text
    file_name = hashlib.md5(schema_text.encode()).hexdigest() + '.md'
    output_path = os.path.join(output_dir, file_name)
    
    with open(output_path, 'w') as f:
        f.write(schema_text)
    print(f"Schema for {csv_file} saved to {output_path}")

def convert(data_dir: str, doc_dir: str, include_rows_num: int) -> None:
    """Main conversion function."""
    csv_files = get_csv_files(data_dir)
    
    for csv_file in csv_files:
        print(f"Processing {csv_file}")
        df = pd.read_csv(csv_file)
        schema = extract_schema(df)
        schema_text = generate_schema_text(schema, csv_file, df, include_rows_num)
        save_schema(schema_text, csv_file, doc_dir)

def main():
    parser = argparse.ArgumentParser(description="Convert CSV files to schema documents")
    parser.add_argument("--data_dir", required=True, help="Directory containing CSV files")
    parser.add_argument("--doc_dir", required=True, help="Output directory for schema documents")
    parser.add_argument("--include-rows-num", type=int, default=0, help="Number of sample rows to include in the schema")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.doc_dir):
        os.makedirs(args.doc_dir)
    
    convert(args.data_dir, args.doc_dir, args.include_rows_num)

if __name__ == "__main__":
    main()