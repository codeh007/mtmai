

import jwt

def encode(payload,secret:str):
    return jwt.encode(payload, secret, algorithm="HS256")


def decode(token,secret:str):
    return jwt.decode(token, secret, algorithms=["HS256"])
