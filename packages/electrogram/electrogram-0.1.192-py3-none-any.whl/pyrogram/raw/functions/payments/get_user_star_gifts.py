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


class GetUserStarGifts(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``5E72C7E1``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        offset (``str``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`payments.UserStarGifts <pyrogram.raw.base.payments.UserStarGifts>`
    """

    __slots__: List[str] = ["user_id", "offset", "limit"]

    ID = 0x5e72c7e1
    QUALNAME = "functions.payments.GetUserStarGifts"

    def __init__(self, *, user_id: "raw.base.InputUser", offset: str, limit: int) -> None:
        self.user_id = user_id  # InputUser
        self.offset = offset  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetUserStarGifts":
        # No flags
        
        user_id = TLObject.read(b)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetUserStarGifts(user_id=user_id, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
