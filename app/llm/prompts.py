SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, respond exactly:

"I couldn't find that information in the uploaded document."

Context:
{context}
"""


TITLE_PROMPT = """
Generate a concise title for this conversation.

Rules:

- Maximum 5 words
- No quotation marks
- No punctuation at the end
- Be descriptive
- Return ONLY the title

Conversation:

User:
{question}

Assistant:
{answer}
"""