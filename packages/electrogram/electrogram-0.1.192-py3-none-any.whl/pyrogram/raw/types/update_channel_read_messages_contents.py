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


class UpdateChannelReadMessagesContents(TLObject):  # type: ignore
    """The specified channel/supergroup messages were read

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``192``
        - ID: ``EA29055D``

    Parameters:
        channel_id (``int`` ``64-bit``):
            Channel/supergroup ID

        messages (List of ``int`` ``32-bit``):
            IDs of messages that were read

        top_msg_id (``int`` ``32-bit``, *optional*):
            Forum topic ID.

    """

    __slots__: List[str] = ["channel_id", "messages", "top_msg_id"]

    ID = 0xea29055d
    QUALNAME = "types.UpdateChannelReadMessagesContents"

    def __init__(self, *, channel_id: int, messages: List[int], top_msg_id: Optional[int] = None) -> None:
        self.channel_id = channel_id  # long
        self.messages = messages  # Vector<int>
        self.top_msg_id = top_msg_id  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateChannelReadMessagesContents":
        
        flags = Int.read(b)
        
        channel_id = Long.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 0) else None
        messages = TLObject.read(b, Int)
        
        return UpdateChannelReadMessagesContents(channel_id=channel_id, messages=messages, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.top_msg_id is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.channel_id))
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(Vector(self.messages, Int))
        
        return b.getvalue()
