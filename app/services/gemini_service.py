import google.generativeai as genai
import os
from app.core.config import settings
import re

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.0-pro')  # Selected a free model

# Token limit for input
TOKEN_LIMIT = 512

def clean_text(text):
    """
    Clean and format the text for readability:
    - Remove all markdown patterns.
    - Remove all newlines (\n).
    - Remove excessive spaces and format as a single continuous block of text.
    """
    # Remove markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italic
    text = re.sub(r'__(.*?)__', r'\1', text)      # Remove underline
    text = re.sub(r'`(.*?)`', r'\1', text)        # Remove inline code
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)   # Remove images
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)    # Remove links

    # Remove all newlines and normalize spaces
    text = text.replace('\n', ' ')               # Replace newlines with spaces
    text = re.sub(r'\s{2,}', ' ', text)          # Replace multiple spaces with a single space

    # Trim leading and trailing whitespace
    text = text.strip()

    return text

def paginate_text(text, token_limit=TOKEN_LIMIT):
    """
    Split the text into smaller chunks based on the token limit.
    """
    words = text.split()
    chunks = [' '.join(words[i:i + token_limit]) for i in range(0, len(words), token_limit)]
    return chunks

def paginate_output(text, page_size=500):
    """
    Paginate the output into chunks of `page_size`.
    """
    return [text[i:i + page_size] for i in range(0, len(text), page_size)]

def gemini_response(text):
    """
    Process the input, send it to the model, and handle the response.
    """
    try:
        # Step 1: Check and paginate input if needed
        if len(text.split()) > TOKEN_LIMIT:
            input_chunks = paginate_text(text, TOKEN_LIMIT)
        else:
            input_chunks = [text]

        responses = []
        for chunk in input_chunks:
            # Step 2: Get the response for each chunk
            response = model.generate_content(chunk)
            cleaned_text = clean_text(response.text)
            responses.append(cleaned_text)

        # Step 3: Combine all responses and paginate the final output
        combined_output = ' '.join(responses)
        pages = paginate_output(combined_output)

        # Return paginated output
        return {
            "total_pages": len(pages),
            "pages": pages
        }
    except Exception as e:
        raise RuntimeError(f"Error while generating content: {e}")