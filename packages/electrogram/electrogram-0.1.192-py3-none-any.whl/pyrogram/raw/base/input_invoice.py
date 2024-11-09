# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputInvoice = Union["raw.types.InputInvoiceChatInviteSubscription", "raw.types.InputInvoiceMessage", "raw.types.InputInvoicePremiumGiftCode", "raw.types.InputInvoiceSlug", "raw.types.InputInvoiceStarGift", "raw.types.InputInvoiceStars"]


class InputInvoice:  # type: ignore
    """An invoice

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            InputInvoiceChatInviteSubscription
            InputInvoiceMessage
            InputInvoicePremiumGiftCode
            InputInvoiceSlug
            InputInvoiceStarGift
            InputInvoiceStars
    """

    QUALNAME = "pyrogram.raw.base.InputInvoice"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
