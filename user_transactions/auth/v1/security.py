from passlib.hash import pbkdf2_sha256


def get_hashed_password(password: str) -> str:
    
    return pbkdf2_sha256.hash(password)


def is_correct_password(password: str, hash_password: str) -> bool:
    
    return pbkdf2_sha256.verify(password, hash_password)