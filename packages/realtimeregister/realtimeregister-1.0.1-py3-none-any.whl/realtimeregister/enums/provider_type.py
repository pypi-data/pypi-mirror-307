from enum import Enum, unique

@unique
class ProviderType(Enum):
    REGISTRY = "registry"
    RESELLER = "reseller"
    INTERNAL = "internal"