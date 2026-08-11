"""
GENERATION
Takes the user's question + the retrieved chunks, builds a prompt, and
calls the LLM to produce a grounded answer with citations.

Built last, after retrieval is working -- this is where "augmentation"
(step 3 in our diagram) happens.
"""


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
    raise NotImplementedError("Build after retrieve.py works.")


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    1. Call build_prompt() to construct the full prompt
    2. Send it to the Anthropic API (client.messages.create(...))
    3. Return the model's text response

    Use ANTHROPIC_API_KEY from app.config here.
    """
    raise NotImplementedError("Build last, once build_prompt works.")
