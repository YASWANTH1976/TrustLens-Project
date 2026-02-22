import pandas as pd
import requests
import io
import os

# Create data folder
if not os.path.exists("data"):
    os.makedirs("data")

# Official Raw Data Links (FakeNewsNet)
urls = {
    "real": "https://raw.githubusercontent.com/KaiDMML/FakeNewsNet/master/dataset/politifact_real.csv",
    "fake": "https://raw.githubusercontent.com/KaiDMML/FakeNewsNet/master/dataset/politifact_fake.csv"
}

print("Downloading dataset... This might take a minute.")
dfs = []

try:
    # Process Real News (Label = 0)
    resp_real = requests.get(urls["real"]).content
    df_real = pd.read_csv(io.StringIO(resp_real.decode('utf-8')))
    df_real['label'] = 0
    dfs.append(df_real[['title', 'label']])

    # Process Fake News (Label = 1)
    resp_fake = requests.get(urls["fake"]).content
    df_fake = pd.read_csv(io.StringIO(resp_fake.decode('utf-8')))
    df_fake['label'] = 1
    dfs.append(df_fake[['title', 'label']])

    # Merge and Save
    master_df = pd.concat(dfs, ignore_index=True)
    master_df.dropna(inplace=True) # Remove empty rows
    master_df.to_csv("data/dataset.csv", index=False)
    print(f"Success! Dataset saved to 'data/dataset.csv' with {len(master_df)} news items.")

except Exception as e:
    print(f"Error: {e}")