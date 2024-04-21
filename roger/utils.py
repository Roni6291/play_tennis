from collections.abc import Iterable
from enum import EnumMeta


def one_hot_encode_enums(enum_: EnumMeta, val: str) -> Iterable[int]:
    """One hot encode enums

    Args:
        enum_ (Enum): Any string enum class
        val (str): a value

    Returns:
        Iterable[int]: one hot encoded iterable
    """
    return [1 if v == val else 0 for _, v in enum_.__members__.items()]
