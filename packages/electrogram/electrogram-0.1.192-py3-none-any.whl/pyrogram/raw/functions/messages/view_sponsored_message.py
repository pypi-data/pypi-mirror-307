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


class ViewSponsoredMessage(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``673AD8F1``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        random_id (``bytes``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "random_id"]

    ID = 0x673ad8f1
    QUALNAME = "functions.messages.ViewSponsoredMessage"

    def __init__(self, *, peer: "raw.base.InputPeer", random_id: bytes) -> None:
        self.peer = peer  # InputPeer
        self.random_id = random_id  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ViewSponsoredMessage":
        # No flags
        
        peer = TLObject.read(b)
        
        random_id = Bytes.read(b)
        
        return ViewSponsoredMessage(peer=peer, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bytes(self.random_id))
        
        return b.getvalue()
