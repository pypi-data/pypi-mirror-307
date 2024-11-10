from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ksxt.models.common import GeneralResponse


class TransactionInfo(BaseModel):
    # 주문 고유 아이디
    uuid: str
    # 주문 종류 (ask, bid, deposit, withdrawal)
    type: str

    # 금액
    amount: float
    # 수수료
    fee: Optional[float] = 0

    # 계좌 번호
    account_id: Optional[str] = None
    # 화폐 통화 정보
    currency: Optional[str] = None

    # 주문 생성 시간
    created_at: datetime


class OpenedOrderInfo(TransactionInfo):
    # 종목 정보
    symbol: str
    # 가격
    price: float
    # 수량
    qty: float
    # 주문 방식
    order_type: Optional[str]


class ClosedOrderInfo(TransactionInfo):
    # 종목 정보
    symbol: str
    # 가격
    price: float
    # 수량
    qty: float
    # 주문 방식
    order_type: Optional[str]


class WithdrawalHistory(BaseModel):
    history: List[TransactionInfo]


class DepositHistory(BaseModel):
    history: List[TransactionInfo]


class OpenedOrderHistory(BaseModel):
    history: List[OpenedOrderInfo]


class ClosedOrderHistory(BaseModel):
    history: List[ClosedOrderInfo]


class KsxtWithdrawalHistoryResponse(GeneralResponse[WithdrawalHistory]):
    pass


class KsxtDepositHistoryResponse(GeneralResponse[DepositHistory]):
    pass


class KsxtOpenOrderResponse(GeneralResponse[OpenedOrderHistory]):
    pass


class KsxtClosedOrderResponse(GeneralResponse[ClosedOrderHistory]):
    pass
