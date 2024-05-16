import hashlib
from util import base62

def make_shorten_url(original_url: str):
    hashed = hashlib.sha512(original_url.encode()).hexdigest()
    if hashed[0] == '0':
        sequence = hashed[1:11]
    else:
        sequence = hashed[:10]
    key = int(sequence, base=16)
    return base62.encode(key)