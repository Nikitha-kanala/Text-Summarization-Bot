

from transformers import pipeline

# Load pre-trained summarization model (BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Take input text from the user
print("Please enter the text you want to summarize (press Enter twice to end):")

# Read multi-line input from the user and join them as a single string
input_text = ""
while True:
    line = input()
    if line:
        input_text += " " + line  # Join lines into a single string with spaces between lines
    else:
        break

# Generate summary
summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)

# Print summary
print("\nSummary:\n", summary[0]['summary_text'])
