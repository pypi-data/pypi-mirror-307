import pandas as pd
import argparse
from topicgpt_python.utils import *
import os

def sample_data(data, out_file, num_sample):
    # Check if file exists
    if not os.path.isfile(data):
        raise FileNotFoundError(f"File not found: {data}")
    
    # Read data
    print(f"Reading from: {data}")
    try:
        df = pd.read_json(data, lines=True)
    except ValueError as e:
        raise ValueError(f"Error reading JSON data: {e}. Check file content.")
    # Proceed with sampling
    df = df.sample(num_sample)
    df.to_json(out_file, lines=True, orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=str,
        default="data/input/bills_subset.jsonl",
        help="data to do topic modeling on",
    )
    parser.add_argument(
        "--num_sample", type=int, default=1000, help="number of samples to generate"
    )
    parser.add_argument(
        "--out_file",
        type=str,
        default="data/input/sample.jsonl",
        help="file containing generation samples",
    )
    args = parser.parse_args()
    sample_data(data, num_sample, out_file)
