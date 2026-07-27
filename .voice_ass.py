import os
import speech_recognition as sr
from gtts import gTTS

# Init recognizer and set parameters manually for a natural feel
rec = sr.Recognizer()
rec.energy_threshold = 300  # Adjust based on ambient noise
rec.dynamic_energy_threshold = True

def capture_voice_input():
    """
    Listens to the microphone, handles ambient noise, 
    and converts speech to text using Google Web Speech API.
    """
    with sr.Microphone() as source:
        print("\n[Listening...] Speak your home appliance issue now:")
        
        # Quick calibration for background noise
        rec.adjust_for_ambient_noise(source, duration=0.8)
        
        try:
            # Capture the audio stream with a timeout limit
            audio_data = rec.listen(source, timeout=5, phrase_time_limit=10)
            
            # Convert audio to arabic text (egyptian dialect context)
            user_speech = rec.recognize_google(audio_data, language="ar-EG")
            print(f"User Said -> {user_speech}")
            return user_speech
            
        except sr.WaitTimeoutError:
            print("[Warning] Listening timed out. No input detected.")
            return None
        except sr.UnknownValueError:
            print("[Error] Could not understand the audio. Please try again.")
            return None
        except sr.RequestError:
            print("[Error] Network connection failed or speech service is down.")
            return None

def speak_bot_output(response_text):
    """
    Converts the textual response from the chatbot 
    into an MP3 audio file and plays it back.
    """
    if not response_text:
        return

    # Generate speech using gTTS
    tts_engine = gTTS(text=response_text, lang='ar', slow=False)
    audio_path = "temp_response.mp3"
    
    # Save and play the audio file
    tts_engine.save(audio_path)
    
    # Simple OS-level execution to play the file (Windows default)
    os.system(f"start {audio_path}")

# Main execution loop
if __name__== "__main__":
    print("=== HomeFix Voice Module Initialized ===")
    
    while True:
        # Get query from microphone
        query = capture_voice_input()
        
        if query:
            # Exit condition
            if "خروج" in query or "exit" in query.lower():
                print("Exiting voice assistant. Goodbye!")
                break
                
            # TODO: Pass this 'query' variable to your RAG pipeline / ChromaDB 
            # to fetch the exact solution from your cleaned CSV dataset.
            
            # Temporary mock response for testing the voice loop
            bot_reply = f"أهلاً بكِ، لقد استلمت مشكلتك وهي: {query}. سأقوم بالبحث عن الحل المناسب الآن."
            
            print(f"Bot Reply -> {bot_reply}")
            
            # Output the reply via speech
            speak_bot_output(bot_reply)