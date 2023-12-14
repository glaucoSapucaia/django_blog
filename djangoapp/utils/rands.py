import string
from random import SystemRandom
from django.utils.text import slugify

def randSlug(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits,
        k=k,
    ))

def slugifyNew(text):
    return slugify(text) + '-' + randSlug()
