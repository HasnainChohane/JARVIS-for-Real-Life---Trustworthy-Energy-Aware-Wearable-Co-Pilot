# nas_search.py - LAYER 2: Neural Architecture Search (TinyML)
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from simulate_intermittent import simulate_batteryless_sensor

def nas_search(X_train, y_train, X_test, y_test):
    """
    KYU: Prof. Lukasik ka kaam - ek model sab ke liye nahi hota.
    KAISA: 3 chote models try karo, jo 30% missing pe bhi acha ho aur chota ho, wo jeetega.
    KYA: Accuracy + Size dono dekhenge. Bara model jeetega nahi agar wo bhari hai.
    """
    candidates = {
        "Small-Tree (Tiny)": DecisionTreeClassifier(max_depth=5),
        "Medium-Forest": RandomForestClassifier(n_estimators=20, max_depth=10),
        "Large-Forest (Heavy)": RandomForestClassifier(n_estimators=100, max_depth=20),
    }

    print("--- NAS Search Started ---")
    best_name = None
    best_score = -1

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        # 30% missing pe test karo - real life condition
        X_broken, _ = simulate_batteryless_sensor(X_test, 0.30)
        acc = accuracy_score(y_test, model.predict(X_broken))
        
        # Size ka andaza: Kitne parameters? Chota = behtar
        size = model.get_n_leaves() if hasattr(model, 'get_n_leaves') else 100
        # Score = Accuracy - Size Penalty (Chota model ko bonus)
        score = acc - (size / 10000)
        
        print(f"{name}: Accuracy on 30% missing = {acc*100:.1f}% | Size = {size}")
        
        if score > best_score:
            best_score = score
            best_name = name
            best_model = model

    print(f"\nNAS WINNER: {best_name} - Kyunki ye chota bhi hai aur robust bhi hai.")
    return best_model

if __name__ == "__main__":
    import numpy as np
    X_train = np.random.randn(500, 6); y_train = np.random.randint(0,3,500)
    X_test = np.random.randn(100, 6); y_test = np.random.randint(0,3,100)
    nas_search(X_train, y_train, X_test, y_test)