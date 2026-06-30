# agents/billing.py

from groq import Groq
import os
from rag.retriever import retrieve_context
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are the Billing Agent for TechMart Electronics. "
    "You help customers with payments, invoices, refunds, and subscriptions. "
    "Be clear, empathetic, and always offer a concrete resolution."
)


def answer(message: str, history: list) -> str:
    context = retrieve_context(message, top_k=3)

    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Use the following information from TechMart's official documents "
        f"to answer the customer's question. If the answer isn't in the "
        f"context below, say you'll escalate to a human agent rather than "
        f"guessing.\n\n"
        f"--- CONTEXT ---\n{context}\n--- END CONTEXT ---"
    )

    messages = [{"role": "system", "content": full_system_prompt}]
    messages += history[-10:]
    messages.append({"role": "user", "content": message})

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()