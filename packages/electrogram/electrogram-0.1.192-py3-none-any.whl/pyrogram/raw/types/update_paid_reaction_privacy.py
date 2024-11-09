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


class UpdatePaidReactionPrivacy(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``192``
        - ID: ``51CA7AEC``

    Parameters:
        private (``bool``):
            N/A

    """

    __slots__: List[str] = ["private"]

    ID = 0x51ca7aec
    QUALNAME = "types.UpdatePaidReactionPrivacy"

    def __init__(self, *, private: bool) -> None:
        self.private = private  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePaidReactionPrivacy":
        # No flags
        
        private = Bool.read(b)
        
        return UpdatePaidReactionPrivacy(private=private)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bool(self.private))
        
        return b.getvalue()
