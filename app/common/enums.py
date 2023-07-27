from __future__ import annotations

import enum


class BlockchainType(enum.Enum):
    ETHEREUM = 'ETHEREUM'
    POLYGON = 'POLYGON'

    @classmethod
    def _synonyms(cls) -> dict[str, BlockchainType]:
        return {'eth': cls.ETHEREUM}

    @classmethod
    def _missing_(cls, value):  # type: ignore
        '''
        This is a workaround for the fact that the Enum class does not
        support synonyms and case-insensitive matching. This method is
        called when the Enum class cannot find a matching name
        '''
        for member in cls:
            if member.value == value.upper():
                return member

        for synonym, member in cls._synonyms().items():
            if synonym == value.lower():
                return member

        return None


class AudienceType(enum.Enum):
    AUDIENCE = 'audience'
    CLAIMED = 'claimed'
    FIXED_LIST = 'fixed_list'
    ANALYTICS = 'analytics'
