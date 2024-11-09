from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class BroadcastRevenueBalances(TLObject):  # type: ignore
    """{schema}

    Constructor of :obj:`~pyrogram.raw.base.BroadcastRevenueBalances`.

    Details:
        - Layer: ``192``
        - ID: ``C3FF71E7``

    Parameters:
        current_balance (``int`` ``64-bit``):
            

        available_balance (``int`` ``64-bit``):
            

        overall_revenue (``int`` ``64-bit``):
            

        withdrawal_enabled (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["current_balance", "available_balance", "overall_revenue", "withdrawal_enabled"]

    ID = 0xc3ff71e7
    QUALNAME = "types.BroadcastRevenueBalances"

    def __init__(self, *, current_balance: int, available_balance: int, overall_revenue: int, withdrawal_enabled: Optional[bool] = None) -> None:
        self.current_balance = current_balance  # long
        self.available_balance = available_balance  # long
        self.overall_revenue = overall_revenue  # long
        self.withdrawal_enabled = withdrawal_enabled  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BroadcastRevenueBalances":
        
        flags = Int.read(b)
        
        withdrawal_enabled = True if flags & (1 << 0) else False
        current_balance = Long.read(b)
        
        available_balance = Long.read(b)
        
        overall_revenue = Long.read(b)
        
        return BroadcastRevenueBalances(current_balance=current_balance, available_balance=available_balance, overall_revenue=overall_revenue, withdrawal_enabled=withdrawal_enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.withdrawal_enabled else 0
        b.write(Int(flags))
        
        b.write(Long(self.current_balance))
        
        b.write(Long(self.available_balance))
        
        b.write(Long(self.overall_revenue))
        
        return b.getvalue()
