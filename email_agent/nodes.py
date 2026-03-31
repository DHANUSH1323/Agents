from langchain_core.messages import HumanMessage
from .state import EmailState
from .config import model


def read_email(state: EmailState) -> dict:
    email = state["email"]
    print(f"Agent is processing an email from {email['sender']} with subject: {email['subject']}")
    return {}


def classify_email(state: EmailState) -> dict:
    email = state["email"]

    prompt = f"""
    As Alfred the butler, analyze this email and determine if it is spam or legitimate.

    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    First, determine if this email is spam. If it is spam, explain why.
    If it is legitimate, categorize it (inquiry, complaint, thank you, etc.).
    """

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    response_text = str(response.content).strip().lower()
    is_spam = "spam" in response_text and "not spam" not in response_text

    spam_reason = None
    if is_spam and "reason:" in response_text:
        spam_reason = response_text.split("reason:")[1].strip()

    email_category = None
    if not is_spam:
        categories = ["inquiry", "complaint", "thank you", "request", "information"]
        for category in categories:
            if category in response_text:
                email_category = category
                break

    new_messages = state.get("messages", []) + [
        {"role": "system", "content": prompt},
        {"role": "assistant", "content": response.content},
    ]

    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": new_messages,
    }


def handle_spam(state: EmailState) -> dict:
    print(f"Agent has marked the email as spam. Reason: {state['spam_reason']}")
    print("The email has been moved to the spam folder.")
    return {}


def draft_response(state: EmailState) -> dict:
    email = state["email"]
    category = state["email_category"] or "general"

    prompt = f"""
    As Alfred the butler, draft a polite preliminary response to this email.

    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    This email has been categorized as: {category}

    Draft a brief, professional response that Mr. Hugg can review and personalize before sending.
    """

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content},
    ]

    return {
        "email_draft": response.content,
        "messages": new_messages,
    }


def notify(state: EmailState) -> dict:
    email = state["email"]

    print("\n" + "=" * 50)
    print(f"Dhanush, you've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print(f"Category: {state['email_category']}")
    print("\nI've prepared a draft response for your review:")
    print("-" * 50)
    print(state["email_draft"])
    print("=" * 50 + "\n")

    return {}
