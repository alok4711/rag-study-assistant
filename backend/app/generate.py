"""
GENERATION
Takes the user's question + the retrieved chunks, builds a prompt, and
calls the LLM to produce a grounded answer with citations.

Built last, after retrieval is working -- this is where "augmentation"
(step 3 in our diagram) happens.
"""

from google import genai
from app.config import GEMINI_API_KEY


def build_prompt(question: str, chunks: list[dict]) -> str:
    """
    Combine the question and retrieved chunks into one prompt for the LLM.

    Things to get right here (this is where most RAG quality problems
    actually come from, more than people expect):
    - Clearly separate each chunk, and label which source file it's from
    - Instruct the model to ONLY answer using the provided chunks, and to
      say "I don't know" if the answer isn't in them (this reduces
      hallucination)
    - Ask it to cite which source(s) it used in the answer
    """
    # 1. Build the context from retrieved chunks and Join chunks with a blank line
    context = ""
    for chunk in chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"

    # 2. Build the final prompt
    prompt = f"""
    You are a study assistant. Answer the question using ONLY the context provided below.

    If the answer is not present in the context, say:
    "I don't know based on the notes provided."

    Do not use outside knowledge or make up information.

    Always mention which source file(s) you used to answer the question.

    Context:
    {context}

    Question: {question}

    Answer:"""

    return prompt


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    1. Call build_prompt() to construct the full prompt
    2. Send it to the GEMINI API (client.messages.create(...))
    3. Return the model's text response

    Use GEMINI_API_KEY from app.config here.
    """

    # 1. Build the complete prompt
    prompt = build_prompt(question, chunks)

    # 2. Create Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # 3. Send the prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    answer_text = response.text
    return answer_text
