

import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline

# Load pre-trained summarization model (BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to generate summary with chunking for any text length
def summarize_text():
    user_input = entry.get("1.0", tk.END).strip()  # Get text from the user input field
    print(f"User input: {user_input}")  # Debugging: Check if input is read correctly
    
    if user_input:
        # Check if the input text is too long (for chunking)
        chunk_size = 1500  # Max length per chunk, can adjust based on model limitations
        if len(user_input) > chunk_size:
            chunks = [user_input[i:i + chunk_size] for i in range(0, len(user_input), chunk_size)]
            print(f"Number of chunks: {len(chunks)}")  # Debugging: Check number of chunks
        else:
            chunks = [user_input]  # If the input is short enough, don't split into chunks
            print("Processing single chunk.")  # Debugging: Indicating it's a single chunk
        
        full_summary = ""

        # Process each chunk (whether it's a single chunk or multiple chunks)
        for chunk in chunks:
            print(f"Processing chunk: {chunk[:50]}...")  # Debugging: Show first 50 characters of the chunk
            
            # Generate summary for the chunk
            summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
            print(f"Generated summary: {summary[0]['summary_text']}")  # Debugging: Show the generated summary for each chunk
            
            full_summary += summary[0]['summary_text'] + " "

        # Display the input and summary in the respective areas
        chat_window.config(state=tk.NORMAL)
        chat_window.delete(1.0, tk.END)  # Clear previous chat history
        chat_window.insert(tk.END, "You: " + user_input + "\n\n")
        
        # Display the summary in a separate text box below
        summary_text.config(state=tk.NORMAL)  # Enable summary text box for updating
        summary_text.delete(1.0, tk.END)  # Clear previous summary
        summary_text.insert(tk.END, "Summary: " + full_summary.strip() + "\n")
        summary_text.config(state=tk.DISABLED)  # Disable editing the summary box after updating
        
        # Disable editing the chat window
        chat_window.config(state=tk.DISABLED)
        
        entry.delete("1.0", tk.END)  # Clear input field after summarizing
    else:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "Bot: Please enter some text to summarize.\n\n")
        chat_window.config(state=tk.DISABLED)

# Initialize main window
window = tk.Tk()
window.title("Summarization Chatbot")
window.geometry("500x600")

# Create a scrolling chat window for user input
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)
chat_window.pack(pady=10)

# Create the input field for user text
entry = tk.Text(window, wrap=tk.WORD, width=60, height=5)
entry.pack(pady=10)

# Create a button to trigger summarization
summarize_button = tk.Button(window, text="Summarize", command=summarize_text)
summarize_button.pack(pady=10)

# Create a separate text box for the summary output
summary_text = tk.Text(window, wrap=tk.WORD, width=60, height=7, state=tk.DISABLED)
summary_text.pack(pady=10)

# Start the GUI loop
window.mainloop()
