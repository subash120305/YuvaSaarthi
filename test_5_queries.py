"""
Test chatbot with 5 specific queries and capture exact responses
"""
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define 5 test queries
test_queries = [
    {
        "id": 1,
        "category": "Fee Structure Query",
        "query": "What is the total annual fee for polytechnic diploma courses in Rajasthan?",
        "system": "You are YuvaSaarthi, an AI assistant for Department of Technical Education, Rajasthan. Provide accurate information about fees, admissions, and courses."
    },
    {
        "id": 2,
        "category": "Eligibility Requirements",
        "query": "What are the minimum eligibility criteria to get admission in polytechnic after 10th class?",
        "system": "You are YuvaSaarthi. Provide clear eligibility information for polytechnic admissions."
    },
    {
        "id": 3,
        "category": "Career Guidance",
        "query": "Which branch should I choose in polytechnic if I want to become a software developer?",
        "system": "You are YuvaSaarthi. Provide helpful career guidance for students."
    },
    {
        "id": 4,
        "category": "Concept Explanation",
        "query": "Explain what is Computer Science Engineering and what subjects are taught in it",
        "system": "You are YuvaSaarthi. Explain engineering programs clearly for students."
    },
    {
        "id": 5,
        "category": "Administrative Help",
        "query": "How can I apply for admission and what documents do I need?",
        "system": "You are YuvaSaarthi. Help students with admission process and document requirements."
    }
]

print("="*70)
print("YUVASAARTHI - 5 QUERY TEST WITH EXACT RESPONSES")
print("="*70)

results = []

for test in test_queries:
    print(f"\n\nQUERY {test['id']}: {test['category']}")
    print("-"*70)
    print(f"Question: {test['query']}")
    print("\nGenerating response...")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": test['system']},
                {"role": "user", "content": test['query']}
            ],
            max_tokens=400,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        print(f"\nYuvaSaarthi's Response:")
        print(answer)

        results.append({
            "query_id": test['id'],
            "category": test['category'],
            "query": test['query'],
            "response": answer,
            "status": "SUCCESS"
        })

    except Exception as e:
        print(f"\nERROR: {e}")
        results.append({
            "query_id": test['id'],
            "category": test['category'],
            "query": test['query'],
            "response": f"Error: {e}",
            "status": "FAILED"
        })

print("\n\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
print(f"\nTotal Queries: 5")
print(f"Successful: {success_count}")
print(f"Failed: {5 - success_count}")

print("\n" + "="*70)
print("Test completed!")
