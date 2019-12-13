from dataclasses import dataclass


@dataclass
class PlayVideo:
    source: str


@dataclass
class QueueVideo:
    source: str


@dataclass
class StopVideo:
    pass


@dataclass
class ToggleVideoState:
    pass


@dataclass
class SeekVideo:
    duration: int


@dataclass
class IncreaseVolume:
    amount: int


@dataclass
class DecreaseVolume:
    amount: int


@dataclass
class NextVideo:
    pass


@dataclass
class PrevVideo:
    pass


@dataclass
class ToggleSubtitle:
    pass


@dataclass
class IncreaseSubtitleDelay:
    pass


@dataclass
class DecreaseSubtitleDelay:
    pass
