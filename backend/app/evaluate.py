import csv
import io

from app.retrieve import retrieve_relevant_chunks
from app.generate import generate_answer


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