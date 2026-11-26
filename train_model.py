import pandas as pd
import numpy as np
import urllib.request
import zipfile
import os
import time
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Downloading real human data...")

# Naya link - zyada stable hai
url = "https://archive.ics.uci.edu/static/public/240/uci+har+dataset.zip"

# 5 dafa try karo
for attempt in range(5):
    try:
        print(f"Trying... {attempt+1}/5")
        urllib.request.urlretrieve(url, "UCI_HAR.zip")
        print("Download done!")
        break
    except Exception as e:
        print(f"Net toot gaya, dobara try kar raha hun... {e}")
        time.sleep(3)
        if attempt == 4:
            print("Bhai net bohot kharab hai, thori dair baad try karo")
            raise e

with zipfile.ZipFile("UCI_HAR.zip", 'r') as zip_ref:
    zip_ref.extractall(".")

print("Unzip done!")

# Load Train Data
X_train = pd.read_csv("UCI HAR Dataset/train/X_train.txt", sep=r'\s+', header=None)
y_train = pd.read_csv("UCI HAR Dataset/train/y_train.txt", sep=r'\s+', header=None)
X_test = pd.read_csv("UCI HAR Dataset/test/X_test.txt", sep=r'\s+', header=None)
y_test = pd.read_csv("UCI HAR Dataset/test/y_test.txt", sep=r'\s+', header=None)

print(f"Training data: {X_train.shape}")

print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train.values.ravel())

accuracy = model.score(X_test, y_test)
print(f"Real Model Accuracy: {accuracy*100:.1f}%")

with open("har_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Saved as har_model.pkl - Your Layer 2 is now REAL!")