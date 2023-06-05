# -*- coding: utf-8 -*-
import re
import PyPDF2
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import openai
from tkinter import Tk, filedialog

# Set your OpenAI API key
openai.api_key = "Your-OPENAI-API-KEY"

def select_pdf_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def remove_graphics(text):
    # Use regular expressions to remove graphics or unwanted characters
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'(\d+)', '', text)  # Remove numbers
    text = re.sub(r'\[[^\]]+\]', '', text)  # Remove text within square brackets
    text = re.sub(r'\([^)]+\)', '', text)  # Remove text within parentheses
    text = re.sub(r'\{[^}]+\}', '', text)  # Remove text within curly braces
    text = re.sub(r'\b[A-Za-z]\b', '', text)  # Remove single characters
    text = re.sub(r'\b[A-Za-z]{1,2}\b', '', text)  # Remove two-letter words

    return text

def process_text(text):
    # Load the English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_sm")

    # Tokenize the text into sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Remove stopwords and perform lemmatization
    cleaned_text = []
    for sentence in sentences:
        words = [token.lemma_ for token in nlp(sentence) if token.text.lower() not in STOP_WORDS]
        cleaned_sentence = ' '.join(words)
        cleaned_text.append(cleaned_sentence)

    return cleaned_text

def remove_contact_info(text):
    # Use regular expressions to remove mobile number and email address
    text = re.sub(r'\b[0-9]{10}\b', '', text)  # Remove 10-digit numbers
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', text)  # Remove email addresses

    return text

# Step 1: Select a PDF file from the computer explorer
file_path = select_pdf_file()

# Step 2: Extract text from the PDF file
pdf_text = extract_text_from_pdf(file_path)

# Step 3: Remove graphics from the extracted text
cleaned_text = remove_graphics(pdf_text)

# Step 4: Process the text (tokenization, stopword removal, lemmatization)
processed_text = process_text(cleaned_text)

# Step 5: Remove contact information (mobile number, email address)
cleaned_text_without_info = remove_contact_info(' '.join(processed_text))

# Step 6: Print the document text
print("Document Text:")
print(pdf_text)
