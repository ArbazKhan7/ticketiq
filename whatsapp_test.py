from app.adapters.whatsapp import handle_whatsapp_message

SESSION_ID = "whatsapp:+971500000001"

def simulate_chat():
    print(handle_whatsapp_message(SESSION_ID, "AC not working"))
    print(handle_whatsapp_message(SESSION_ID, "My name is Perwez"))
    print(handle_whatsapp_message(SESSION_ID, "234"))
    # STOP here — ticket is complete

if __name__ == "__main__":
    simulate_chat()
