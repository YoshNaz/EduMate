import json
import sqlite3
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Path to SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "instance", "test.db")


def fetch_summary(file_id):
    """Fetch summarized text from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT summary FROM summaries WHERE file_id = ?", (file_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def card_gen(file_id, num_flashcards=5):
    
    summarized_text = fetch_summary(file_id)
    if not summarized_text or summarized_text.strip() == "":
        return json.dumps({"error": "No summary found for this file ID"}, indent=4)

    print("Fetched Summary:", summarized_text)

    # OpenAI Prompt
    prompt = f"""
    Generate {num_flashcards} educational flashcards from the following text.
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
                    "content": "You are an AI that generates educational flashcards.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        raw_output = response["choices"][0]["message"]["content"]
        print("Model Output:", raw_output)  # Debugging Output

        # Extract flashcards
        flashcards = []
        lines = raw_output.split("\n")
        question, answer = None, None

        for line in lines:
            line = line.strip()

            if line.startswith("Q:"):
                if question and answer:  # Store previous flashcard before resetting
                    flashcards.append({"question": question, "answer": answer})
                question = line.replace("Q:", "").strip()
                answer = None  # Reset answer

            elif line.startswith("A:") or (question and not answer):
                answer = line.replace("A:", "").strip()

        # Append the last flashcard
        if question and answer:
            flashcards.append({"question": question, "answer": answer})

        print("Extracted Flashcards:\n", json.dumps(flashcards, indent=4))

        if not flashcards:
            return json.dumps({"error": "No valid flashcards generated"}, indent=4)

        return json.dumps(flashcards, indent=4)

    except openai.error.OpenAIError as e:
        return json.dumps({"error": str(e)}, indent=4)


# Run Test
if __name__ == "__main__":
    file_id = 3  # Replace with actual file ID
    flashcards_json = card_gen(file_id)
    print(flashcards_json)
