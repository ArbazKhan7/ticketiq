import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_openai():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict JSON tester."},
            {"role": "user", "content": "Return JSON with key status='ok'."}
        ],
        temperature=0
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    test_openai()
