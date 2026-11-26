# baseline_har.py - LAYER 2: Baseline Model
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from simulate_intermittent import simulate_batteryless_sensor

def train_and_test():
    """
    KYU: Baseline bina liye hum NAS ko justify nahi kar sakte.
    KAISA: Pehle 0% missing pe train, phir 30% missing pe test.
    """
    # STEP 1: Fake data banao (Asli me yahan UCI HAR dataset aayega)
    # 0=Walking, 1=Sitting, 2=Running
    np.random.seed(42)
    X_train = np.random.randn(1000, 6)
    y_train = np.random.randint(0, 3, 1000)
    X_test = np.random.randn(300, 6)
    y_test = np.random.randint(0, 3, 300)

    # STEP 2: Model train karo - Normal data pe
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)

    # STEP 3: Normal test - 0% missing
    acc_clean = accuracy_score(y_test, model.predict(X_test))
    print(f"Clean Data (0% missing): {acc_clean*100:.1f}% Accuracy")

    # STEP 4: Batteryless test - 30% missing
    X_broken, missing = simulate_batteryless_sensor(X_test, 0.30)
    acc_broken = accuracy_score(y_test, model.predict(X_broken))
    print(f"Batteryless Data (30% missing): {acc_broken*100:.1f}% Accuracy")
    print(f"PROBLEM PROVED: Accuracy {acc_clean*100:.1f}% -> {acc_broken*100:.1f}% gir gayi!")
    print("Isi liye hume NAS + Trust chahiye.")

if __name__ == "__main__":
    train_and_test()