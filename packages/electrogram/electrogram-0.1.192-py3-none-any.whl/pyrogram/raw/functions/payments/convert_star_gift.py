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


class ConvertStarGift(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``421E027``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["user_id", "msg_id"]

    ID = 0x421e027
    QUALNAME = "functions.payments.ConvertStarGift"

    def __init__(self, *, user_id: "raw.base.InputUser", msg_id: int) -> None:
        self.user_id = user_id  # InputUser
        self.msg_id = msg_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ConvertStarGift":
        # No flags
        
        user_id = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        return ConvertStarGift(user_id=user_id, msg_id=msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(Int(self.msg_id))
        
        return b.getvalue()
