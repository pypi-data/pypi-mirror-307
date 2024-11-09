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


class KeyboardButtonRequestPoll(TLObject):  # type: ignore
    """A button that allows the user to create and send a poll when pressed; available only in private

    Constructor of :obj:`~pyrogram.raw.base.KeyboardButton`.

    Details:
        - Layer: ``192``
        - ID: ``BBC7515D``

    Parameters:
        text (``str``):
            Button text

        quiz (``bool``, *optional*):
            If set, only quiz polls can be sent

    """

    __slots__: List[str] = ["text", "quiz"]

    ID = 0xbbc7515d
    QUALNAME = "types.KeyboardButtonRequestPoll"

    def __init__(self, *, text: str, quiz: Optional[bool] = None) -> None:
        self.text = text  # string
        self.quiz = quiz  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonRequestPoll":
        
        flags = Int.read(b)
        
        quiz = Bool.read(b) if flags & (1 << 0) else None
        text = String.read(b)
        
        return KeyboardButtonRequestPoll(text=text, quiz=quiz)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.quiz is not None else 0
        b.write(Int(flags))
        
        if self.quiz is not None:
            b.write(Bool(self.quiz))
        
        b.write(String(self.text))
        
        return b.getvalue()
