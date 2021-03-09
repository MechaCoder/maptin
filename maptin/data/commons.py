from string import ascii_letters, digits, punctuation
from random import choices, randint
from hashlib import md5, sha1, sha512
from typing import Dict, Mapping

from argon2 import PasswordHasher
from validators import email as validatorEmail
from validators import url as validatorUrl
from validators.utils import ValidationFailure

def makeUid(hex_length: int = 8, complex:bool = False):

    pool = ascii_letters + digits
    
    if complex:
        pool += punctuation

    poolSize = hex_length * randint(10, 40)
    hex = choices(pool, k=poolSize)
    hex = choices(pool, k=hex_length)
    return ''.join(hex)

def simpleHash(planeText):

    b = bytes(planeText, 'utf-8')
    r_md5 = md5(b).hexdigest()
    b = bytes(r_md5, 'utf-8')
    r_sha1 = sha1(b).hexdigest()
    r_sha512 = sha512(
        bytes(r_sha1, 'utf-8')
    ).hexdigest()

    return r_sha512

def makePassword(planeText:str, salt:str):
    pw = simpleHash(planeText + salt)
    pw = PasswordHasher().hash(pw)
    return pw

def verfyPassword(planeText: str, salt: str, hash: str):
    pw = simpleHash(planeText + salt)
    return PasswordHasher().verify(hash=hash, password=pw)

def vaildateEmail(email: str):
    try:
        return validatorEmail(email)
    except ValidationFailure:
        return False

def vaildateUrl(addr):
    try:
        if 'youtube' not in addr:
            return False

        if 'watch=' not in addr:
            return False

        return vaildateUrl(addr)
    except ValidationFailure:
        return False

class Document(Dict):

    def __init__(self, value: Mapping, doc_id: int):
        super().__init__(value)
        self.doc_id = doc_id