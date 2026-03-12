from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_memory_response(context, question):

    prompt = f"""
You are a helpful assistant for Alzheimer's patients.

Use the memory information below to answer the question clearly and gently.

Memory Context:
{context}

Question:
{question}

Answer in a simple and comforting way.
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text


def generate_ai_response(prompt):

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text