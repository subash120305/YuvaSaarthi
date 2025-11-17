"""
YuvaSaarthi - Interactive Demo
Test your chatbot with real queries!
"""

import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment
from dotenv import load_dotenv
load_dotenv()

from groq import Groq


def print_separator():
    print("\n" + "="*70)


def demo():
    """Run interactive demo"""
    print_separator()
    print("         YUVASAARTHI - AI EDUCATIONAL ASSISTANT")
    print_separator()
    print("\nWelcome! This demo shows YuvaSaarthi's capabilities.")
    print("\nFeatures:")
    print("  - Multilingual (English, Hindi, Rajasthani)")
    print("  - Educational Q&A")
    print("  - Concept Explanations")
    print("  - Powered by Groq (Llama 3.3 70B)")

    # Initialize client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Demo queries
    test_queries = [
        {
            "lang": "English",
            "question": "What are the admission requirements for polytechnic?",
            "system": "You are YuvaSaarthi, an educational assistant for the Department of Technical Education, Government of Rajasthan. Answer questions about admissions professionally."
        },
        {
            "lang": "Hindi",
            "question": "पाइथागोरस प्रमेय को सरल भाषा में समझाइए",
            "system": "You are YuvaSaarthi, a friendly educational assistant. Explain concepts in simple Hindi for students."
        },
        {
            "lang": "English (Concept)",
            "question": "Explain Newton's First Law of Motion in simple terms for a Class 10 student",
            "system": "You are a friendly tutor. Explain physics concepts simply and encouragingly."
        }
    ]

    for i, query in enumerate(test_queries, 1):
        print_separator()
        print(f"\nDEMO {i}: {query['lang']} Query")
        print_separator()
        print(f"\nQuestion: {query['question']}")
        print("\nThinking...")

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": query['system']},
                    {"role": "user", "content": query['question']}
                ],
                max_tokens=300,
                temperature=0.7
            )

            answer = response.choices[0].message.content
            print(f"\nYuvaSaarthi: {answer}")

        except Exception as e:
            print(f"\nError: {e}")

    # Interactive mode
    print_separator()
    print("\nINTERACTIVE MODE")
    print_separator()
    print("\nNow YOU can ask questions!")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("\nYour Question: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for trying YuvaSaarthi!")
                print_separator()
                break

            if not user_input:
                continue

            # Detect rough language
            is_hindi = any(ord(char) > 0x0900 and ord(char) < 0x097F for char in user_input)

            system_prompt = "You are YuvaSaarthi, a helpful educational assistant for students in Rajasthan. Answer questions about education, courses, and academic concepts."

            if is_hindi:
                system_prompt += " Respond in Hindi."

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=300,
                temperature=0.7
            )

            answer = response.choices[0].message.content

            # Try to print safely
            try:
                print(f"\nYuvaSaarthi: {answer}")
            except UnicodeEncodeError:
                # Fallback for Windows console encoding issues
                safe_answer = answer.encode('ascii', 'replace').decode('ascii')
                print(f"\nYuvaSaarthi: {safe_answer}")
                print("\n(Note: Some characters couldn't display due to console encoding)")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\nDemo error: {e}")
        print("\nMake sure:")
        print("1. .env file exists with GROQ_API_KEY")
        print("2. Internet connection is working")
        print("3. All dependencies are installed")
