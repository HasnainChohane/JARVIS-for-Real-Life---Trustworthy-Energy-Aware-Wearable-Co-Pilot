# copilot_llm.py - LAYER 4: Activity-Adaptive Co-Pilot
def generate_response(activity, calibrated_conf, missing_rate):
    """
    KYU: User walking hai to uska dimag busy hai. Lamba jawab = stress.
    KAISA: Activity dekh ke jawab ka size badlo.
    KYA: Walking = 3 words. Sitting = Full detail. Running = Chup.
    """
    # Pehle Trust check karo
    if calibrated_conf < 0.60:
        return f"I'm only {calibrated_conf*100:.0f}% sure you are {activity} because {missing_rate*100:.0f}% sensor data is missing. Are you {activity}? [Yes/No]"

    # Ab Activity ke hisab se jawab
    if activity == "WALKING":
        return "Turn left. [Short - Kyunki tum walk kar rahe ho, dimag busy hai]"
    elif activity == "SITTING":
        return "You are sitting for 2 hours. Your heart rate is high. I suggest a 5-min walk in 10 min because long sitting is bad for health. [Long - Kyunki tum free ho]"
    elif activity == "RUNNING":
        return "[SILENT] - Tum running kar rahe ho, me chup hun, baad me bataunga. [Silent - Kyunki tum busy ho]"
    else:
        return f"You are {activity}."

if __name__ == "__main__":
    print(generate_response("WALKING", 0.54, 0.40))
    print("---")
    print(generate_response("SITTING", 0.90, 0.05))
    print("---")
    print(generate_response("RUNNING", 0.85, 0.10))