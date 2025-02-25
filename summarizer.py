from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from transformers import BartForConditionalGeneration, BartTokenizer
import io  # To handle BytesIO

# Load AI model
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")


def summarize(file_content, file_name):
    text = ""

    # **Check File Type Based on Extension**
    if file_name.lower().endswith(".pdf"):
        try:
            pdf_document = fitz.open("pdf", file_content)
            for page in pdf_document:
                text += page.get_text("text") + "\n"

            if not text.strip():
                return "No readable text found in PDF."

        except Exception as e:
            return f"Error processing PDF: {e}"

    elif file_name.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            image = Image.open(io.BytesIO(file_content))  # Open image from BytesIO

            # Extract text using OCR
            text = pytesseract.image_to_string(image, config="--psm 6")

            if not text.strip():
                return "No readable text found in the image."

        except Exception as e:
            return f"Error processing image: {e}"

    else:
        return (
            "Unsupported file format. Please upload a PDF or an image (PNG, JPG, JPEG)."
        )

    # If there's no text, return an error message
    if not text.strip():
        return "No readable text found in the file."

    # Tokenize the extracted text
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

    # Decode summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Format key points
    short_notes = summary.split(". ")
    short_notes = [f"- {note.strip()}" for note in short_notes if note]

    formatted_notes = (
        f"# Summary Notes\n{summary}\n\n### Key Points\n{chr(10).join(short_notes)}"
    )

    return formatted_notes
