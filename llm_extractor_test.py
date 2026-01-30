from app.services.llm_extractor import extract_ticket_fields

def test_llm_extractor():
    message = (
        "Hi, my name is Perwez. "
        "I live in Tower A, flat 234. "
        "My AC is not working and needs urgent attention."
    )

    result = extract_ticket_fields(message)
    print(result)


if __name__ == "__main__":
    test_llm_extractor()
