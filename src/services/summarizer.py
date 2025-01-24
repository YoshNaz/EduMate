import fitz  # PyMuPDF


def pdf_to_text(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open ("U:\Project Repo\EduMate\data\interim\Testdata.pdf")
    text = ""

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    return text

