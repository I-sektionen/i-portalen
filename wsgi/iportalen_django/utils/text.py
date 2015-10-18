import string
import random


def count_words(text):
    return len(text.split())


def count_characters(text):
    return len(text)


def random_string_generator(size=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))