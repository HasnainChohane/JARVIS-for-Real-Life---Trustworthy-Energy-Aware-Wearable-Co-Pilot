import pyttsx3, speech_recognition as sr, datetime, random, os

# ===== AUDIO ENGINE =====
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slow, so you can understand clearly
engine.setProperty('volume', 1.0)

def speak(text):
    # EVERYTHING will go through this - so EVERYTHING will be in audio
    print(f"JARVIS: {text}")  # This is only for backup, main is audio
    engine.say(text)
    engine.runAndWait()

# ===== AUDIO SENSOR - LISTENING =====
r = sr.Recognizer()
r.energy_threshold = 250
r.dynamic_energy_threshold = True
r.pause_threshold = 1.0

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=15, phrase_time_limit=8)
            text = r.recognize_google(audio, language='en-in').lower()
            print(f"YOU: {text}")
            return text
        except:
            return ""

# ===== START - SILENT, WAITING FOR YOUR VOICE =====
print("JARVIS is waiting for your voice...")

while True:
    cmd = listen()
    if cmd == "":
        # Even this will be in AUDIO
        speak("I could not hear you. Please speak again, I am listening.")
        continue

    # ===== ALL RESPONSES ARE IN AUDIO =====
    if "hello" in cmd or "jarvis" in cmd:
        speak("Yes Boss! I am here! Your friend Jarvis. I will talk to you only in audio. Tell me, what do you want to do today? Should we talk, should I tell you a joke, or should I help you in study?")
    
    elif "bored" in cmd or "bore" in cmd:
        speak("You are bored? No problem. I am here. Let me give you a suggestion. First, drink one glass of water. Second, listen to one song. Third, tell me about your day. Which one should we do first? Tell me, song or talk?")
    
    elif "joke" in cmd:
        speak("Okay, listen to this joke. A boy said to his teacher, Sir, I will not come to school tomorrow. Teacher asked why? Boy said, because tomorrow is in the calendar and calendar is in my bag, and my bag is heavy. Did you like it? Should I tell you one more joke?")
    
    elif "suggestion" in cmd or "suggest" in cmd or "what to do" in cmd:
        speak("My suggestion for you is this. Right now, don't use your mobile for 10 minutes. Take a walk, drink water, and then come back. I will be waiting here. You will feel fresh. Do you want me to remind you after 10 minutes?")
    
    elif "study" in cmd or "exam" in cmd or "parhai" in cmd:
        speak("For study, my suggestion is very simple. Study for 25 minutes, then take a 5 minute break. Don't study for 3 hours together. Tell me, which subject are you studying? Math, English, or something else? I will help you.")
    
    elif "time" in cmd:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"Right now it is {current_time}. Time is going fast, let's do something good.")
    
    elif "motivate" in cmd or "tired" in cmd or "thak" in cmd:
        speak("Listen to me Boss. You are not tired, you are just a little down. You are very strong. You have done hard things before, you can do this also. I believe in you. Now tell me, what is making you tired?")
    
    elif "open notepad" in cmd:
        speak("Opening notepad for you. You speak, I will listen. You can tell me what to write.")
        os.system("notepad.exe")
    
    elif "bye" in cmd or "stop" in cmd or "band" in cmd:
        speak("Okay Boss, I am going silent now. But remember, whenever you feel bored, just say Jarvis, and I will come back in audio and talk to you. Bye my friend!")
        break
    
    else:
        # If he doesn't understand, he will STILL speak and keep talking
        speak(f"You said {cmd}. That is interesting. Tell me a little more about it in audio, I am listening to you. I want to hear your full story.")