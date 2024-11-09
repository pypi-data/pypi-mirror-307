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


class KeyboardButtonWebView(TLObject):  # type: ignore
    """Button to open a bot mini app using messages.requestWebView, sending over user information after user confirmation.

    Constructor of :obj:`~pyrogram.raw.base.KeyboardButton`.

    Details:
        - Layer: ``192``
        - ID: ``13767230``

    Parameters:
        text (``str``):
            Button text

        url (``str``):
            Web app url

    """

    __slots__: List[str] = ["text", "url"]

    ID = 0x13767230
    QUALNAME = "types.KeyboardButtonWebView"

    def __init__(self, *, text: str, url: str) -> None:
        self.text = text  # string
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonWebView":
        # No flags
        
        text = String.read(b)
        
        url = String.read(b)
        
        return KeyboardButtonWebView(text=text, url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        b.write(String(self.url))
        
        return b.getvalue()
