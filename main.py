import numpy as np
import pickle
from simulate_intermittent import simulate_batteryless_sensor


print("=== JARVIS - 2 Sensor, Alag Alag Data ===\n")

with open("har_model.pkl", "rb") as f:
    model = pickle.load(f)

# Sensor 1 - Haath wala - WALKING bol raha hai
sensor1 = np.random.normal(loc=[0.8, 0.5, 0.2, 1.2, 0.9, 0.4], scale=0.2, size=(1, 6))

# Sensor 2 - Jeb wala - SITTING bol raha hai - DEKHO YE ALAG HAI
sensor2 = np.random.normal(loc=[0.1, 0.1, 0.9, 0.2, 0.1, 0.1], scale=0.1, size=(1, 6))

names = ["WALKING", "SITTING", "LAYING"]

# Dono se alag alag poocho
pred1 = model.predict(sensor1)[0]
pred2 = model.predict(sensor2)[0]

print(f"Sensor 1 (Haath) bola: {names[pred1]}")
print(f"Sensor 2 (Jeb) bola: {names[pred2]}")

# Layer 1 - Missing
_, missing1 = simulate_batteryless_sensor(np.repeat(sensor1, 100, axis=0), 0.50)
_, missing2 = simulate_batteryless_sensor(np.repeat(sensor2, 100, axis=0), 0.10)
missing = (missing1 + missing2) / 2
print(f"\n[Layer 1] Total Missing = {missing*100:.0f}%")

# Layer 2 + 3 - Agar dono lad rahe hain to confidence gira do
if pred1 != pred2:
    print(f"\n[Layer 2] ARRE! Dono sensor lad rahe hain! Ek keh raha {names[pred1]}, dusra {names[pred2]}")
    # Dono ka average le lo, lekin confidence aadha kar do kyunki jhagra ho raha hai
    sensor_data = (sensor1 + sensor2) / 2
    confidence = np.max(model.predict_proba(sensor_data)[0]) * 0.5  # Jhagre ki saza
    print(f"[Layer 3] Jhagre ki wajah se Confidence 50% gira diya, ab {confidence*100:.0f}% reh gaya")
    activity = names[pred1]  # Filhal pehle wale ki maan lo
else:
    print(f"\n[Layer 2] Dono sensor ek hi baat bol rahe hain, Good!")
    sensor_data = (sensor1 + sensor2) / 2
    confidence = np.max(model.predict_proba(sensor_data)[0])
    activity = names[pred1]

calibrated = confidence * (1 - missing)
print(f"[Layer 3] Calibrated = {calibrated*100:.0f}%")

# Layer 4
ask_human = calibrated < 0.60
if ask_human:
    print(f"\n[Layer 4] JARVIS: I'm only {calibrated*100:.0f}% sure... Mere dono sensor lad rahe hain. Are you {activity}? [Yes/No]")
    answer = input("Tum bolo (Yes/No): ")
    if answer.lower() == "yes":
        print("[Layer 4] JARVIS: Shukriya! Ab me seekh gaya.")
    else:
        correct = input("Tum kya kar rahe the? (WALKING/SITTING/LAYING): ")
        print(f"[Layer 4] JARVIS: Ok, {correct} yaad kar liya!")
else:
    print(f"\n[Layer 4] JARVIS: Turn left, you are {activity}")