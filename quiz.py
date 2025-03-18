import json
import sqlite3
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PATH = os.path.join(os.path.dirname(__file__), "instance", "test.db")


def fetch_summary(file_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT summary FROM summaries WHERE file_id = ?", (file_id,)
            )
            result = cursor.fetchone()

        if result:
            print(f"Fetched summary for file_id {file_id}: {result[0]}")
            return result[0]
        else:
            print(f"No summary found for file_id {file_id}")
            return None
    except Exception as e:
        print(f"Database error: {e}")
        return None


def quiz_gen(file_id, num_questions=5):
    summarized_text = fetch_summary(file_id)
    if not summarized_text or not summarized_text.strip():
        return json.dumps({"error": "No summary found for this file ID"}, indent=4)

    print("Fetched Summary:", summarized_text)

   
    prompt = f"""
    Generate {num_questions} quiz questions from the following text.
    Format the response as:
    
    Q: [Question]
    A: [Answer]

    Text:
    {summarized_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that generates quiz questions.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        raw_output = (
            response.get("choices", [{}])[0].get("message", {}).get("content", "")
        )
        print("Model Output:", raw_output)  

        
        quiz = []
        lines = raw_output.split("\n")
        question, answer = None, None

        for line in lines:
            if line.startswith("Q: "):
                if question and answer:
                    quiz.append(
                        {"question": question, "answer": answer}
                    )  
                question = line[3:].strip()
                answer = None
            elif line.startswith("A: ") and question:
                answer = line[3:].strip()

        if question and answer:
            quiz.append({"question": question, "answer": answer})

        return json.dumps({"quiz": quiz}, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)
