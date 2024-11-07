from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class Price:
    workday: str
    code: str
    price: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    volume_amt: int
    time: str = None
    hightime: str = None
    lowtime: str = None

@dataclass(frozen=True)
class Hoga:
    price: int
    qty: int

@dataclass(frozen=True)
class OrderBook:
    code: str
    total_buy: int
    total_sell: int
    buy: List[Hoga] = field(default_factory=list)
    sell: List[Hoga] = field(default_factory=list)