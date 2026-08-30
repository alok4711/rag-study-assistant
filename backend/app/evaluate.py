import csv
import io

from app.retrieve import retrieve_relevant_chunks
from app.generate import generate_answer

from app.config import GEMINI_API_KEY
from google import genai


def parse_test_set(csv_text: str) -> list[dict]:
    """
    Parse CSV text (question,expected_answer columns) into a list of dicts:
    [{"question": "...", "expected_answer": "..."}, ...]
    """

    reader = csv.DictReader(io.StringIO(csv_text))

    test_set = []

    for row in reader:
        question = row.get("question")
        expected_answer = row.get("expected_answer")

        # Skip rows with missing or empty values
        if not question or not expected_answer:
            continue

        # Strip whitespace once
        question = question.strip()
        expected_answer = expected_answer.strip()

        # Skip empty/whitespace-only values
        if not question or not expected_answer:
            continue

        test_set.append({
            "question": question,
            "expected_answer": expected_answer
        })

    return test_set


def get_actual_answers(test_set: list[dict], db_path: str) -> list[dict]:
    """
    For each {"question", "expected_answer"} in test_set, run it through
    the RAG pipeline to get the actual answer produced by the app.

    Returns a list of dicts, each extending the input with an "actual_answer" key:
    [{"question": ..., "expected_answer": ..., "actual_answer": ...}, ...]
    """

    results = []

    for item in test_set:

        chunks = retrieve_relevant_chunks(item["question"], db_path)

        actual_answer = generate_answer(item["question"], chunks)

        result = {**item, "actual_answer": actual_answer}

        results.append(result)

    return results


def judge_answer(question: str, expected_answer: str, actual_answer: str) -> dict:
    """
    Uses Gemini to score how well actual_answer matches expected_answer.
    Returns {"score": int, "reasoning": str}
    """


    prompt = f"""
    You are an evaluator judging whether an AI-generated answer is correct.

    Question: {question}
    Expected Answer: {expected_answer}
    Actual Answer: {actual_answer}

    Score the actual answer on a scale of 1-5:
    5 = Fully correct and matches the expected answer's meaning
    3 = Partially correct, missing some detail
    1 = Incorrect or contradicts the expected answer

    Respond in EXACTLY this format, nothing else:
    Score: <number>
    Reasoning: <one sentence explanation>

    Do not add any introduction, conclusion, markdown, or additional text.
    """

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    try:
        score_text = text.split("Score:")[1].split("Reasoning:")[0].strip()
        reasoning = text.split("Reasoning:")[1].strip()
        score = int(score_text)
    except (IndexError, ValueError):
        # Model didn't follow the format -- don't crash the whole eval run,
        # just record it as unparseable and keep going
        score = 0
        reasoning = f"Could not parse judge response: {text[:100]}"

    return {
        "score": score,
        "reasoning": reasoning
    }


def run_evaluation(csv_text: str, db_path: str) -> list[dict]:
    """
    Full evaluation pipeline: parse CSV -> get actual answers -> judge each one.

    Returns a list of dicts, each with:
    question, expected_answer, actual_answer, score, reasoning
    """

    test_set = parse_test_set(csv_text)

    results_with_actuals = get_actual_answers(test_set, db_path)

    final_results = []

    for item in results_with_actuals:
        
        judge_result = judge_answer(item["question"], item["expected_answer"], item["actual_answer"])

        evaluated_item = {**item, **judge_result}

        final_results.append(evaluated_item)

    return final_results