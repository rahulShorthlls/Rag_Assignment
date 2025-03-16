import pandas as pd
import requests
import json

def fetch_answer(question, url="http://127.0.0.1:5000/ask"):
    try:
        payload = {"question": question}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("answer", "No response")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    
    if "query" not in df.columns:
        print("Error: 'query' column not found in CSV file.")
        return
    
    df["response"] = df["query"].apply(fetch_answer)
    df.to_csv(output_file, index=False)
    print(f"Processed file saved as {output_file}")

# Example usage
input_csv = "output.csv"   # Replace with your CSV file
output_csv = "generated.csv" # Replace with your desired output file
process_csv(input_csv, output_csv)
