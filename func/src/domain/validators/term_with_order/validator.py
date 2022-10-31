# Jormungandr
from ...enums.types import TermType, QuoteType


# Third party
from pydantic import BaseModel


class Order(BaseModel):
    symbol: str
    quantity: int
    quote_type: QuoteType


class TermWithOrder(BaseModel):
    order: Order
    term_type: TermType
