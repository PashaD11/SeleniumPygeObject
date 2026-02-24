from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: str
    id: int = None
    brand: str = None
    category: dict = None
    cart_quantity: int = None
