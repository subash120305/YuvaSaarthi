"""
Test script to verify bot is using new knowledge bases
"""
import os
from dotenv import load_dotenv
load_dotenv()

from backend.chatbot_engine import ChatbotEngine

# Initialize chatbot
print("Initializing chatbot...")
chatbot = ChatbotEngine()

# Test queries that should pull from new knowledge bases
test_queries = [
    {
        "query": "What is the reservation percentage for SC category in Rajasthan?",
        "expected_info": "Should mention 16% from new KB"
    },
    {
        "query": "What is the minimum percentage required to pass Class 10 RBSE exam?",
        "expected_info": "Should mention 33% from new KB"
    },
    {
        "query": "What is the EWS income limit for reservation?",
        "expected_info": "Should mention 8 lakh from new KB"
    }
]

print("\n" + "="*60)
print("Testing Bot with New Knowledge Base")
print("="*60 + "\n")

for i, test in enumerate(test_queries, 1):
    print(f"[TEST {i}] {test['query']}")
    print(f"Expected: {test['expected_info']}")
    print("\nGenerating response...")

    try:
        result = chatbot.process_query(
            query=test['query'],
            user_id="test_user",
            language="en",
            include_videos=False
        )

        response = result.get('response', '')
        print(f"\nBot Response:\n{response}\n")
        print("-"*60 + "\n")

    except Exception as e:
        print(f"\nERROR: {e}\n")
        print("-"*60 + "\n")

print("\n[SUCCESS] All tests completed!")
print("If responses mention specific details from the new KB, integration is working!\n")
