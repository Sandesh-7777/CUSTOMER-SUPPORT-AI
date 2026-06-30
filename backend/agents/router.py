# agents/router.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VALID_INTENTS = {"billing", "technical", "product", "complaint", "faq"}


def detect_intent(message: str) -> str:
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intent classifier for a customer support system. "
                    "Read the customer message and respond with EXACTLY ONE WORD "
                    "from this list, with no punctuation, no explanation, no extra text:\n\n"
                    "billing - payments, refunds, invoices, subscriptions, charges\n"
                    "technical - login issues, bugs, errors, installation, app not working\n"
                    "product - product features, pricing, specs, comparisons, availability\n"
                    "complaint - frustration, dissatisfaction, poor experience, wanting to escalate\n"
                    "faq - general company info, policies, contact info, hours, shipping times\n\n"
                    "Respond with only the single matching word."
                ),
            },
            {"role": "user", "content": message},
        ],
        max_tokens=100,
        temperature=0,
    )
    raw_output = response.choices[0].message.content.strip().lower()

    # DEBUG: print what the model actually returned, so we can see what's happening
    print(f"[INTENT DEBUG] message='{message}' -> raw_output='{raw_output}'")

    # Clean up common issues: punctuation, extra words
    cleaned = raw_output.strip(".,!?\"'").split()[0] if raw_output else ""

    if cleaned in VALID_INTENTS:
        return cleaned

    print(f"[INTENT DEBUG] Could not match '{raw_output}' to a valid intent, defaulting to faq")
    return "faq"