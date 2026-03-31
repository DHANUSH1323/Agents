from langgraph.graph import StateGraph, START, END
from .state import EmailState
from .nodes import read_email, classify_email, handle_spam, draft_response, notify
from .router import route_email

email_graph = StateGraph(EmailState)

email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)
email_graph.add_node("handle_spam", handle_spam)
email_graph.add_node("draft_response", draft_response)
email_graph.add_node("notify", notify)

email_graph.add_edge(START, "read_email")
email_graph.add_edge("read_email", "classify_email")

email_graph.add_conditional_edges(
    "classify_email",
    route_email,
    {
        "spam": "handle_spam",
        "legitimate": "draft_response",
    },
)

email_graph.add_edge("handle_spam", END)
email_graph.add_edge("draft_response", "notify")
email_graph.add_edge("notify", END)

compiled_graph = email_graph.compile()
