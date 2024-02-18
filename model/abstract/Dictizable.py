from __future__ import annotations

from model.abstract.DictDeserializable import DictDeserializable
from model.abstract.DictSerializable import DictSerializable


class Dictizable(DictSerializable, DictDeserializable):
    ...
