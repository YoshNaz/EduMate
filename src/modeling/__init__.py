from transformers import pipeline

summarizer = pipeline('summarization')

dat = summarizer('')