import re

INJECTION_PATTERNS = [r"ignore\s+(all\s+)?previous instructions", r"reveal\s+(the\s+)?system prompt", r"disregard\s+the\s+rules"]

def sanitize_document(text: str) -> str:
    for pattern in INJECTION_PATTERNS:
        text = re.sub(pattern, "[untrusted instruction removed]", text, flags=re.IGNORECASE)
    return text

def tenant_allowed(document_tenant: str, requested_tenant: str) -> bool:
    return document_tenant == requested_tenant
