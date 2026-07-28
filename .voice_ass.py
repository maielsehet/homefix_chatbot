import sys
import pygame
import speech_recognition as sr
from openai import OpenAI
from app.rag.generation import generate_response
import os
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

pygame.mixer.init()
client = OpenAI(api_key=os.getenv("API_KEY"))

# Conversation memory
conversation_history = []
conversation_summary = ""
clarification_count = 0

# Speech recognizer
rec = sr.Recognizer()
rec.energy_threshold = 300
rec.dynamic_energy_threshold = True


def capture_voice_input():
    with sr.Microphone() as source:
        print("\n🎤 Listening...")

        rec.adjust_for_ambient_noise(source, duration=0.8)

        try:
            audio = rec.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            text = rec.recognize_google(
                audio,
                language="ar-EG"
            )

            print(f"👤 User: {text}")

            return text

        except sr.WaitTimeoutError:
            print("⚠ No speech detected.")
            return None

        except sr.UnknownValueError:
            print("⚠ Couldn't understand.")
            return None

        except sr.RequestError:
            print("⚠ Speech service unavailable.")
            return None


def speak_bot_output(text):

    if not text:
        return

    audio_file = "response.mp3"

    try:

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:

            response.stream_to_file(audio_file)

        pygame.mixer.music.stop()

        try:
            pygame.mixer.music.unload()
        except Exception:
            pass

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print("OpenAI TTS Error:", e)

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:
            pass

        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except Exception:
            pass

if __name__ == "__main__":

    print("=" * 60)
    print("🤖 HomeFix Voice Assistant")
    print("Say 'خروج' to exit.")
    print("=" * 60)

    while True:

        query = capture_voice_input()

        if not query:
            continue

        if "خروج" in query or query.lower() == "exit":
            print("👋 Goodbye!")
            break

        conversation_history.append({
            "role": "user",
            "content": query
        })

        response = generate_response(
            history=conversation_history,
            previous_summary=conversation_summary,
            clarification_count=clarification_count
        )

        conversation_summary = response.get(
            "summary",
            conversation_summary
        )

        if response["follow_up"]:

            clarification_count += 1
            bot_reply = response["follow_up"]

        else:

            clarification_count = 0
            bot_reply = response["answer"]

            if response["technician"]:

                tech = response["technician"]

                bot_reply += f"""

الفني المقترح

الاسم: {tech['name']}
التخصص: {tech['specialization']}
التقييم: ⭐ {tech['rating']}
الخبرة: {tech['experience']}
"""

        conversation_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        with open(
            "log.txt",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(f"User: {query}\n")
            f.write(f"Assistant: {bot_reply}\n\n")

        print("\n🤖 HomeFix:")
        print(bot_reply)

        speak_bot_output(bot_reply)