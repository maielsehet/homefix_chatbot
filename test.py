import sys
from app.rag.generation import generate_response

# Support Arabic in Windows Terminal
sys.stdout.reconfigure(encoding="utf-8")

conversation_history = []

print("=" * 60)
print("🤖 HomeFix Assistant")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    user_input = input("\n👤 You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = generate_response(conversation_history)

    print(f"\n🤖 HomeFix:\n{response}")

    conversation_history.append({
        "role": "assistant",
        "content": response
    })