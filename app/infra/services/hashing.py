import secrets

import bcrypt

from app.domain.hash.entity import HashableValue
from app.domain.hash.hash_repository_protocol import HashProtocol



class ServerHashProvider(HashProtocol):
    @staticmethod
    def random_hash(lenb: int = 32) -> HashableValue: 
        token = secrets.token_urlsafe(lenb).encode()
        crypt = bcrypt.hashpw(token, bcrypt.gensalt())
        return HashableValue(crypt)
    
    @staticmethod
    def hash_value(value: HashableValue) -> HashableValue: 
        crypt = bcrypt.hashpw(value.bvalue, bcrypt.gensalt())
        return HashableValue(
            crypt
        )
    
    @staticmethod
    def compare_hash(raw_value: HashableValue, hash: HashableValue) -> bool:
        return bcrypt.checkpw(raw_value.bvalue, hash.bvalue)
    