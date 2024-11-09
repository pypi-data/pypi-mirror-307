# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PrivacyRule = Union["raw.types.PrivacyValueAllowAll", "raw.types.PrivacyValueAllowChatParticipants", "raw.types.PrivacyValueAllowCloseFriends", "raw.types.PrivacyValueAllowContacts", "raw.types.PrivacyValueAllowPremium", "raw.types.PrivacyValueAllowUsers", "raw.types.PrivacyValueDisallowAll", "raw.types.PrivacyValueDisallowChatParticipants", "raw.types.PrivacyValueDisallowContacts", "raw.types.PrivacyValueDisallowUsers"]


class PrivacyRule:  # type: ignore
    """Privacy rules together with privacy keys indicate what can or can't someone do and are specified by a PrivacyRule constructor, and its input counterpart InputPrivacyRule.

    Constructors:
        This base type has 10 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            PrivacyValueAllowAll
            PrivacyValueAllowChatParticipants
            PrivacyValueAllowCloseFriends
            PrivacyValueAllowContacts
            PrivacyValueAllowPremium
            PrivacyValueAllowUsers
            PrivacyValueDisallowAll
            PrivacyValueDisallowChatParticipants
            PrivacyValueDisallowContacts
            PrivacyValueDisallowUsers
    """

    QUALNAME = "pyrogram.raw.base.PrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
