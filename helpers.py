import random
import string


def generate_random_email():
    random_digits = ''.join(random.choice(string.digits) for _ in range(4))
    return f"stameska{random_digits}@yandex.ru"