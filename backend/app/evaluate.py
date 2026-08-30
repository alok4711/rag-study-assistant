import csv
import io


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
            "question": question.strip(),
            "expected_answer": expected_answer.strip()
        })

    return test_set