from pwdlib import PasswordHash

passwordhash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return passwordhash.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return passwordhash.verify(password, hashed_password)
