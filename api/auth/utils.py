import datetime as dt

import jwt

from api.auth.keys_generator import generate_keys


pem_private_key, pem_public_key = generate_keys()


def encode_jwt(
        payload: dict,
        private_key: bytes = pem_private_key,
        algorithm: str = 'RS256',
        expire_minutes: int = 60
) -> str:
    to_encode = payload.copy()
    now = dt.datetime.now(dt.UTC)
    expire = now + dt.timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=expire)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
        token: str,
        public_key: bytes = pem_public_key,
        algorithm: str = 'RS256'
) -> dict:
    try:
        return jwt.decode(token, public_key, algorithms=[algorithm])
    except jwt.exceptions.InvalidTokenError:
        return {}
