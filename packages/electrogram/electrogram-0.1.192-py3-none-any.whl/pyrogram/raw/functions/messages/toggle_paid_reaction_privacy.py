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


class TogglePaidReactionPrivacy(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``849AD397``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        private (``bool``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "msg_id", "private"]

    ID = 0x849ad397
    QUALNAME = "functions.messages.TogglePaidReactionPrivacy"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, private: bool) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.private = private  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePaidReactionPrivacy":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        private = Bool.read(b)
        
        return TogglePaidReactionPrivacy(peer=peer, msg_id=msg_id, private=private)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Bool(self.private))
        
        return b.getvalue()
