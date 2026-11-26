import numpy as np

def simulate_batteryless_sensor(data, missing_rate=0.40, burst_len=10):
    data = data.copy()
    n_samples = data.shape[0]
    
    # NAYA TAREEKA: Pehle decide karo kitne samples gayab karne hain
    total_to_drop = int(n_samples * missing_rate)
    
    # Phir random jagah chunno, bina overlap ke
    all_indices = np.arange(n_samples)
    np.random.shuffle(all_indices)
    drop_indices = all_indices[:total_to_drop]
    
    # Ab unko 0 karo
    data[drop_indices] = 0
    
    # Asli missing nikalo
    actual_missing = np.mean(np.all(data == 0, axis=1))
    return data, actual_missing