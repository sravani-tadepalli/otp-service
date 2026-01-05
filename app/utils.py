import random
import hashlib

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
