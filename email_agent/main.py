from .graph import compiled_graph

legitimate_email = {
    "sender": "john.smith@example.com",
    "subject": "Question about your services",
    "body": (
        "Dear Mr. Hugg, I was referred to you by a colleague and I'm interested in learning more "
        "about your consulting services. Could we schedule a call next week? Best regards, John Smith"
    ),
}

spam_email = {
    "sender": "winner@lottery-intl.com",
    "subject": "YOU HAVE WON $5,000,000!!!",
    "body": (
        "CONGRATULATIONS! You have been selected as the winner of our international lottery! "
        "To claim your $5,000,000 prize, please send us your bank details and a processing fee of $100."
    ),
}

_initial_state = {
    "is_spam": None,
    "spam_reason": None,
    "email_category": None,
    "email_draft": None,
    "messages": [],
}


if __name__ == "__main__":
    print("\nProcessing legitimate email...")
    compiled_graph.invoke({"email": legitimate_email, **_initial_state})

    print("\nProcessing spam email...")
    compiled_graph.invoke({"email": spam_email, **_initial_state})
