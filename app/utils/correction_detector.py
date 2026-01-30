# app/utils/correction_detector.py

CORRECTION_KEYWORDS = [
    "sorry",
    "actually",
    "mistake",
    "wrong",
    "it is",
    "correction",
    "my bad",
    "instead"
]


def is_correction_message(text: str) -> bool:
    if not text:
        return False

    text = text.lower()
    return any(keyword in text for keyword in CORRECTION_KEYWORDS)
