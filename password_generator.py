import random
import string
import math
import pyperclip

DEFAULT_SPECIALS = "!@#$%^&*()"

def generate_password(length=12, letters=True, digits=True, specials=True):
    chars = ""
    if letters:
        chars += string.ascii_letters
    if digits:
        chars += string.digits
    if specials:
        chars += DEFAULT_SPECIALS
    if not chars:
        return "Ошибка: вы не выбрали ни один тип символов!"
    return "".join(random.choice(chars) for _ in range(length))

def estimate_entropy(length, pool_size):
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)

def strength_label(entropy_bits):
    if entropy_bits < 28:
        return "Очень слабый"
    elif entropy_bits < 36:
        return "Слабый"
    elif entropy_bits < 60:
        return "Средний"
    else:
        return "Сильный"

def assess_password(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in DEFAULT_SPECIALS for c in password):
        pool += len(DEFAULT_SPECIALS)
    others = [c for c in password if not (c.isalnum() or c in DEFAULT_SPECIALS)]
    pool += len(set(others))
    pool = max(pool, 1)
    entropy = estimate_entropy(len(password), pool)
    return {
        "entropy_bits": round(entropy, 2),
        "label": strength_label(entropy),
        "pool": pool
    }
