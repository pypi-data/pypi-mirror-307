from pydantic import BaseModel
from typing import List

from ksxt.models.common import GeneralResponse


class BalanceData(BaseModel):
    symbol: str
    name: str
    evaluation_price: float
    price: float
    pnl_amount: float
    pnl_ratio: float
    qty: float
    free_qty: float
    used_qty: float


class BalanceInfo(BaseModel):
    currency: str
    total_amount: float
    total_evaluation_amount: float
    total_pnl_amount: float
    total_pnl_ratio: float
    balances: List[BalanceData]


# Balance에 대한 구체적인 Response 타입
class KsxtBalanceResponse(GeneralResponse[BalanceInfo]):
    pass
