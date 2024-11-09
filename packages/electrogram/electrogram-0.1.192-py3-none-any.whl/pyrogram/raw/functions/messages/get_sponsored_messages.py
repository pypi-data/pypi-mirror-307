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


class GetSponsoredMessages(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``192``
        - ID: ``9BD2F439``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

    Returns:
        :obj:`messages.SponsoredMessages <pyrogram.raw.base.messages.SponsoredMessages>`
    """

    __slots__: List[str] = ["peer"]

    ID = 0x9bd2f439
    QUALNAME = "functions.messages.GetSponsoredMessages"

    def __init__(self, *, peer: "raw.base.InputPeer") -> None:
        self.peer = peer  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSponsoredMessages":
        # No flags
        
        peer = TLObject.read(b)
        
        return GetSponsoredMessages(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
