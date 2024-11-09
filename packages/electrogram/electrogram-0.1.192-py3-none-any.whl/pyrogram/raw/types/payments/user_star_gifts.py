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


class UserStarGifts(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.UserStarGifts`.

    Details:
        - Layer: ``192``
        - ID: ``6B65B517``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        gifts (List of :obj:`UserStarGift <pyrogram.raw.base.UserStarGift>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        next_offset (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetUserStarGifts
    """

    __slots__: List[str] = ["count", "gifts", "users", "next_offset"]

    ID = 0x6b65b517
    QUALNAME = "types.payments.UserStarGifts"

    def __init__(self, *, count: int, gifts: List["raw.base.UserStarGift"], users: List["raw.base.User"], next_offset: Optional[str] = None) -> None:
        self.count = count  # int
        self.gifts = gifts  # Vector<UserStarGift>
        self.users = users  # Vector<User>
        self.next_offset = next_offset  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserStarGifts":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        gifts = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        users = TLObject.read(b)
        
        return UserStarGifts(count=count, gifts=gifts, users=users, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.gifts))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
