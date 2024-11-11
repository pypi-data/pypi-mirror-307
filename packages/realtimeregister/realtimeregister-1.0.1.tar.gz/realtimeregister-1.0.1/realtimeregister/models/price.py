from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class Price:
    product: str
    action: str
    currency: str
    price: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Price':
        return cls(
            product=data['product'],
            action=data['action'],
            currency=data['currency'],
            price=data['price']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'product': self.product,
            'action': self.action,
            'currency': self.currency,
            'price': self.price
        }

@dataclass
class Pricelist:
    prices: List[Price]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pricelist':
        return cls(
            prices=[Price.from_dict(price) for price in data['prices']]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'prices': [price.to_dict() for price in self.prices]
        }