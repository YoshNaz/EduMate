import openai


def generate_flashcard_gpt(text):
    prompt = f"Generate a flashcard question and answer from this text:\n\n{text}\n\nFormat: Q: [question] A: [answer]"

    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "system", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]


print(generate_flashcard_gpt(summary))
