from app.storage.redis import get_session, save_session, clear_session

SESSION_ID = "test-session-123"

def test_redis():
    print("Saving session...")
    save_session(SESSION_ID, {"step": "name", "value": "Perwez"})

    print("Fetching session...")
    data = get_session(SESSION_ID)
    print("Data:", data)

    print("Clearing session...")
    clear_session(SESSION_ID)

    data_after = get_session(SESSION_ID)
    print("After clear:", data_after)


if __name__ == "__main__":
    test_redis()
