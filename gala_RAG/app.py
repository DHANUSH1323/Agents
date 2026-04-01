from typing import Any, Dict, cast
from datasets import load_dataset
from langchain_core.documents import Document

guest_dataset = load_dataset("agents-course/unit3-invitees", split="train")

docs = []
for row in guest_dataset:
    guest = cast(Dict[str, Any], row)
    docs.append(
        Document(
            page_content="\n".join([
                f"Name: {guest['name']}",
                f"Relation: {guest['relation']}",
                f"Description: {guest['description']}",
                f"Email: {guest['email']}"
            ]),
            metadata={"name": guest["name"]},
        )
    )