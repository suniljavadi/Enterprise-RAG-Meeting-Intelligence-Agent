import hashlib
import math
import re

DIMENSIONS = 128

def embed(text: str) -> list[float]:
    vector = [0.0] * DIMENSIONS
    for token in re.findall(r"[a-z0-9_]+", text.lower()):
        index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % DIMENSIONS
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]

def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
