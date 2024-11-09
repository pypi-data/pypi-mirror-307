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


class GetBroadcastRevenueWithdrawalUrl(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``9DF4FAAD``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        password (:obj:`InputCheckPasswordSRP <pyrogram.raw.base.InputCheckPasswordSRP>`):
            N/A

    Returns:
        :obj:`BroadcastRevenueWithdrawalUrl <pyrogram.raw.base.BroadcastRevenueWithdrawalUrl>`
    """

    __slots__: List[str] = ["peer", "password"]

    ID = 0x9df4faad
    QUALNAME = "functions.messages.GetBroadcastRevenueWithdrawalUrl"

    def __init__(self, *, peer: "raw.base.InputPeer", password: "raw.base.InputCheckPasswordSRP") -> None:
        self.peer = peer  # InputPeer
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBroadcastRevenueWithdrawalUrl":
        # No flags
        
        peer = TLObject.read(b)
        
        password = TLObject.read(b)
        
        return GetBroadcastRevenueWithdrawalUrl(peer=peer, password=password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.password.write())
        
        return b.getvalue()
