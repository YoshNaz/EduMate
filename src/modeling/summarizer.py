
from PIL import Image
import pytesseract
from transformers import BartForConditionalGeneration, BartTokenizer

model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

image = Image.open(r'U:\Project Repo\EduMate\data\textbook.png')

text = pytesseract.image_to_string(image)

inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

# Generate summary
summary_ids = model.generate(
    inputs["input_ids"],
    max_length=1024,
    min_length=100,
    length_penalty=1.5,
    num_beams=4,
    early_stopping=True,
)


summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)


short_notes = summary.split(". ")
short_notes = [f"- {note.strip()}" for note in short_notes if note]


formatted_notes = (
    f"# Summary Notes\n{summary}\n\n### Key Points\n{chr(10).join(short_notes)}"
)

print(formatted_notes)
