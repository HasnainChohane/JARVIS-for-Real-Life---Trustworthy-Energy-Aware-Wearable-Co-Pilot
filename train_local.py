import pandas as pd
import zipfile
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Local file se training...")

# Agar zip abhi bhi zip me hai to kholo
import os
if not os.path.exists("UCI HAR Dataset"):
    with zipfile.ZipFile("uci+har+dataset.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
    print("Unzip ho gaya!")

X_train = pd.read_csv("UCI HAR Dataset/train/X_train.txt", sep=r'\s+', header=None)
y_train = pd.read_csv("UCI HAR Dataset/train/y_train.txt", sep=r'\s+', header=None)
X_test = pd.read_csv("UCI HAR Dataset/test/X_test.txt", sep=r'\s+', header=None)
y_test = pd.read_csv("UCI HAR Dataset/test/y_test.txt", sep=r'\s+', header=None)

print(f"Data mil gaya: {X_train.shape}")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train.values.ravel())

accuracy = model.score(X_test, y_test)
print(f"Real Model Accuracy: {accuracy*100:.1f}%")

with open("har_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Ho gaya! har_model.pkl ban gaya.")