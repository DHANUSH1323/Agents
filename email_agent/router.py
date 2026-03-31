from .state import EmailState


def route_email(state: EmailState) -> str:
    """Determine the next step based on spam classification."""
    return "spam" if state["is_spam"] else "legitimate"
