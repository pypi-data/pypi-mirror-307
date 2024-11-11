from enum import Enum, unique

@unique
class CertificateType(Enum):
    DV = "dv"
    OV = "ov"
    EV = "ev"
    WILDCARD = "wildcard"