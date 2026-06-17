from typing import Protocol

from app.domain.hash.entity import HashableValue


class HashProtocol(Protocol):
    
    @staticmethod
    def random_hash(lenb: int = 32) -> HashableValue: ... 
        
    @staticmethod
    def hash_value(value: HashableValue) -> HashableValue: ...
        
    @staticmethod
    def compare_hash(raw_value: HashableValue, hash: HashableValue) -> bool: ...
     