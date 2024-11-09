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


class SimpleWebViewResultUrl(TLObject):  # type: ignore
    """Contains the webview URL with appropriate theme parameters added

    Constructor of :obj:`~pyrogram.raw.base.SimpleWebViewResultUrl`.

    Details:
        - Layer: ``192``
        - ID: ``882F76BB``

    Parameters:
        url (``str``):
            URL

    """

    __slots__: List[str] = ["url"]

    ID = 0x882f76bb
    QUALNAME = "types.SimpleWebViewResultUrl"

    def __init__(self, *, url: str) -> None:
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SimpleWebViewResultUrl":
        # No flags
        
        url = String.read(b)
        
        return SimpleWebViewResultUrl(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        return b.getvalue()
