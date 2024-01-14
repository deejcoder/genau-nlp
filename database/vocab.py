from typing import Optional

from tortoise import fields
from database.base import BaseModel


stored_part_of_speech_tags = [
    'verb',
    'noun',
    'adj',
    'adv'
]


class Vocab(BaseModel):
    id = fields.IntField(pk=True)
    lex = fields.CharField(max_length=255)
    part_of_speech = fields.CharField(max_length=50)
    frequency = fields.IntField()
    weight = fields.FloatField()


class Repository:
    @staticmethod
    async def find_by_lex_and_pos(lex: str, pos: str) -> list[Vocab]:
        """
        Finds existing vocab based on lex and pos
        :param lex:
        :param pos:
        :return: a list of vocab records
        """
        return await Vocab.filter(lex=lex, part_of_speech=pos)\
            .all()

    @staticmethod
    async def take_most_common(num: int, pos: str) -> list[Vocab]:
        """
        Takes the top-most known vocab based on weight and frequency
        :param num:
        :param pos:
        :return: A list of vocab
        """
        return await Vocab.filter(part_of_speech=pos)\
            .order_by('-weight', '-frequency')\
            .limit(num)\
            .all()

    @classmethod
    async def add_or_update_vocab(cls, lex: str, pos: str) -> Optional[Vocab]:
        """
        Adds or updates an existing vocab record
        :param lex:
        :param pos:
        :return: The new record or None when the item is invalid
        """
        if not cls.is_stored_pos_tag(pos):
            return None

        vocab = await cls._get_existing(lex, pos)
        if vocab is None:
            return await Vocab.create(
                lex=lex,
                part_of_speech=pos,
                frequency=1,
                weight=1
            )

        vocab.frequency += 1
        await vocab.save()

    @classmethod
    async def _get_existing(cls, lex: str, pos: str) -> Vocab:
        return await Vocab.filter(lex=lex, part_of_speech=pos).first()

    @classmethod
    def is_stored_pos_tag(cls, pos: str) -> bool:
        if pos.lower() not in stored_part_of_speech_tags:
            return False
        return True


