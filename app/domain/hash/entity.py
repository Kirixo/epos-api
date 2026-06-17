from dataclasses import dataclass


@dataclass(frozen=True)
class HashableValue:
    bvalue: bytes

    def to_hex(self) -> str:
        return self.bvalue.hex()
    
    def to_str(self) -> str:
        return self.bvalue.decode()
    
    @staticmethod
    def from_str(value: str) -> "HashableValue":
        return HashableValue(
            bvalue=value.encode()
        )
        
    @staticmethod
    def from_hex(hex_value: str) -> "HashableValue":
        return HashableValue(
            bvalue=bytes.fromhex(hex_value)
        )