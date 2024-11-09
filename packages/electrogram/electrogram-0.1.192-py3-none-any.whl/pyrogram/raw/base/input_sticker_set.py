# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputStickerSet = Union["raw.types.InputStickerSetAnimatedEmoji", "raw.types.InputStickerSetAnimatedEmojiAnimations", "raw.types.InputStickerSetDice", "raw.types.InputStickerSetEmojiChannelDefaultStatuses", "raw.types.InputStickerSetEmojiDefaultStatuses", "raw.types.InputStickerSetEmojiDefaultTopicIcons", "raw.types.InputStickerSetEmojiGenericAnimations", "raw.types.InputStickerSetEmpty", "raw.types.InputStickerSetID", "raw.types.InputStickerSetPremiumGifts", "raw.types.InputStickerSetShortName"]


class InputStickerSet:  # type: ignore
    """Represents a stickerset

    Constructors:
        This base type has 11 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            InputStickerSetAnimatedEmoji
            InputStickerSetAnimatedEmojiAnimations
            InputStickerSetDice
            InputStickerSetEmojiChannelDefaultStatuses
            InputStickerSetEmojiDefaultStatuses
            InputStickerSetEmojiDefaultTopicIcons
            InputStickerSetEmojiGenericAnimations
            InputStickerSetEmpty
            InputStickerSetID
            InputStickerSetPremiumGifts
            InputStickerSetShortName
    """

    QUALNAME = "pyrogram.raw.base.InputStickerSet"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
