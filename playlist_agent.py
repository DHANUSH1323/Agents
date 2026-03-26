import enable_langfuse_tracing  # noqa: F401

from smolagents import CodeAgent, tool, InferenceClientModel
# from huggingface_hub import login

# login()

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."


agent = CodeAgent(tools=[suggest_menu], model=InferenceClientModel())

agent.run("Prepare a normal meal for party.")