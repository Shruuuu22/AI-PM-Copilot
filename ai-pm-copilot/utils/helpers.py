import re


def redact_pii(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[REDACTED_EMAIL]', text)
    text = re.sub(r'\+?\d[\d\-\s]{6,}\d', '[REDACTED_PHONE]', text)
    return text
