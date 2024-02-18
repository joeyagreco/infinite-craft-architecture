from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from model.abstract.Dictizable import Dictizable


@dataclass(kw_only=True, eq=False)
class Waze(Dictizable):
    waze: str
    timestamp_utc: datetime = field(
        default_factory=lambda: datetime.utcnow()
    )  # autogenerate timestamp on init if not given

    def to_dict(self) -> dict:
        return {"waze": self.waze, "timestamp_utc": self.timestamp_utc.isoformat()}

    @staticmethod
    def from_dict(d: dict) -> Waze:
        timestamp_utc = d["timestamp_utc"]
        if isinstance(timestamp_utc, str):
            timestamp_utc = datetime.fromisoformat(timestamp_utc)
        return Waze(waze=d["waze"], timestamp_utc=timestamp_utc)
