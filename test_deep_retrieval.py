"""
Test if RAG can retrieve specific information from deep within documents
"""
import os
from dotenv import load_dotenv
load_dotenv()

from backend.chatbot_engine import ChatbotEngine

# Initialize chatbot
print("Testing deep document retrieval...")
print("="*60 + "\n")

chatbot = ChatbotEngine()

# Test queries for specific details buried in the comprehensive KB
test_queries = [
    {
        "query": "What is the creamy layer income limit for OBC reservation?",
        "info": "This specific detail is deep in the reservation policy section"
    },
    {
        "query": "What are the subjects in Class 9 half-yearly mathematics exam?",
        "info": "This is a specific section detail from RBSE syllabus"
    },
    {
        "query": "What is the link to check RBSE result online?",
        "info": "Specific URL buried in the KB"
    }
]

for i, test in enumerate(test_queries, 1):
    print(f"[TEST {i}] {test['query']}")
    print(f"Context: {test['info']}\n")

    try:
        result = chatbot.process_query(
            query=test['query'],
            user_id="test_user",
            language="en",
            include_videos=False
        )

        response = result.get('response', '')
        # Safe print for Windows console
        try:
            print(f"Bot Response: {response}\n")
        except:
            print(f"Bot Response: [Response generated but contains special characters]\n")

        print("-"*60 + "\n")

    except Exception as e:
        print(f"ERROR: {e}\n")
        print("-"*60 + "\n")

print("\n[SUCCESS] Deep retrieval test completed!")
print("If bot answered specific details from deep within KB, retrieval works!")
