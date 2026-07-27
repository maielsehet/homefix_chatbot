import os
import speech_recognition as sr
from gtts import gTTS
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import glob
import pygame
import sys
sys.stdout.reconfigure(encoding="utf-8")

pygame.mixer.init()
# Load the multilingual model (works well with Arabic)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Load your cleaned CSV dataset (adjust path/columns to match yours)
csv_files = glob.glob("Data/CSV files/*.csv")
df_list=[pd.read_csv(f, encoding="utf-8-sig") for f in csv_files]# لازم يكون فيه عمود بالمشاكل وعمود بالحلول
df=pd.concat(df_list, ignore_index=True).drop_duplicates()
#problems = df["problem"].tolist()
problems = (df["category"] + " - " + df["problem"]).tolist()
solutions = df["solution"].tolist()

# Precompute embeddings for all problems once at startup
problem_embeddings = model.encode(problems, convert_to_tensor=True)

def get_best_solution(query, threshold=0.3):
    """
    Encodes the user's query and finds the most semantically similar
    problem in the dataset using cosine similarity.
    """
    query_embedding = model.encode(query, convert_to_tensor=True)
    #similarities = util.cos_sim(query_embedding, problem_embeddings)[0]
    query_with_context = df['category'].iloc[0] + " " + query
    query_embedding = model.encode(query_with_context, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, problem_embeddings)[0]

    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()

    if best_score < threshold:
        return "معلش، مش لاقياله حل واضح في الداتا بتاعتي، ممكن توضح المشكلة أكتر؟"
    
    return solutions[best_idx]

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

        #bot_reply = get_best_solution(query)
        #print(f"Bot Reply -> {bot_reply}")
        #speak_bot_output(bot_reply)
        
    # Generate speech using gTTS
    tts_engine = gTTS(text=response_text, lang='ar', slow=False)
    audio_path = "temp_response.mp3"
    
    # Stop and unload any currently playing audio first
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    
    # Save and play the audio file
    tts_engine.save(audio_path)
    
    # Simple OS-level execution to play the file (Windows default)
    #os.system(f"start {audio_path}")

    #play and wait until finished
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
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
            #bot_reply = f"أهلاً بكِ، لقد استلمت مشكلتك وهي: {query}. سأقوم بالبحث عن الحل المناسب الآن."
            #bot_reply = get_best_solution(query)
            solution = get_best_solution(query)
            bot_reply = f"أهلا وسهلا!: {solution}"
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"User Said: {query}\n")
                f.write(f"Bot Reply: {bot_reply}\n")
            
            print(f"Bot Reply -> {bot_reply}")
            
            # Output the reply via speech
            speak_bot_output(bot_reply)