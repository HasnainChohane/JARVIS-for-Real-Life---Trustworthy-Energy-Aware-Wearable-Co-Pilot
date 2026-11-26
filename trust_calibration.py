# trust_calibration.py - LAYER 3: Trust Layer
def calibrate_confidence(raw_confidence, missing_rate):
    """
    KYU: Model 90% bolta hai lekin 40% data gayab hai, to asal confidence 90% nahi hai.
    KAISA: Formula: Calibrated = Raw * (1 - Missing)
    KYA: Agar 90% * (1 - 0.40) = 54% -> Matlab AI ko khud nahi pata.
    """
    calibrated = raw_confidence * (1 - missing_rate)
    return calibrated

def should_ask_human(calibrated_conf, threshold=0.60):
    """
    KYU: Agar AI ko khud nahi pata, to usko insaan se poochna chahiye, jhoot nahi bolna chahiye.
    KAISA: 60% se neeche = Insaan se poocho. 60% se upar = Answer do.
    """
    return calibrated_conf < threshold

# TEST
if __name__ == "__main__":
    # Case 1: Walking, 40% missing
    raw = 0.90; missing = 0.40
    cal = calibrate_confidence(raw, missing)
    print(f"Case 1: Raw 90% | Missing 40% -> Calibrated {cal*100:.0f}%")
    print(f"Ask Human? {should_ask_human(cal)} -> Haan, kyunki 54% < 60%")

    # Case 2: Sitting, 5% missing
    raw = 0.95; missing = 0.05
    cal = calibrate_confidence(raw, missing)
    print(f"\nCase 2: Raw 95% | Missing 5% -> Calibrated {cal*100:.0f}%")
    print(f"Ask Human? {should_ask_human(cal)} -> Nahi, 90% kafi hai")