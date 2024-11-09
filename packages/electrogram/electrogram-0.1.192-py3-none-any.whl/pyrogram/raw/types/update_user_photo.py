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


class UpdateUserPhoto(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``192``
        - ID: ``F227868C``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        photo (:obj:`UserProfilePhoto <pyrogram.raw.base.UserProfilePhoto>`):
            N/A

        previous (``bool``):
            N/A

    """

    __slots__: List[str] = ["user_id", "date", "photo", "previous"]

    ID = 0xf227868c
    QUALNAME = "types.UpdateUserPhoto"

    def __init__(self, *, user_id: int, date: int, photo: "raw.base.UserProfilePhoto", previous: bool) -> None:
        self.user_id = user_id  # long
        self.date = date  # int
        self.photo = photo  # UserProfilePhoto
        self.previous = previous  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateUserPhoto":
        # No flags
        
        user_id = Long.read(b)
        
        date = Int.read(b)
        
        photo = TLObject.read(b)
        
        previous = Bool.read(b)
        
        return UpdateUserPhoto(user_id=user_id, date=date, photo=photo, previous=previous)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(Int(self.date))
        
        b.write(self.photo.write())
        
        b.write(Bool(self.previous))
        
        return b.getvalue()
