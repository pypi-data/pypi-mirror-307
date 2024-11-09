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


class AppWebViewResultUrl(TLObject):  # type: ignore
    """Contains the link that must be used to open a direct link Mini App.

    Constructor of :obj:`~pyrogram.raw.base.AppWebViewResultUrl`.

    Details:
        - Layer: ``192``
        - ID: ``3C1B4F0D``

    Parameters:
        url (``str``):
            The URL to open

    """

    __slots__: List[str] = ["url"]

    ID = 0x3c1b4f0d
    QUALNAME = "types.AppWebViewResultUrl"

    def __init__(self, *, url: str) -> None:
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AppWebViewResultUrl":
        # No flags
        
        url = String.read(b)
        
        return AppWebViewResultUrl(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        return b.getvalue()
