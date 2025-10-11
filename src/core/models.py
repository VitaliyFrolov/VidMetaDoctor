from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------
#  Класс для хранения метаданных видео.
# ---------------------------------------------------

@dataclass
class VideoMetadata:
    filepath: str
    title: Optional[str] = None
    artist: Optional[str] = None 
    comment: Optional[str] = None
    codec: Optional[str] = None
    duration: Optional[float] = None

    def __str__(self):
        return (f"VideoMetadata(filepath={self.filepath}, "
                f"title={self.title}, artist={self.artist}, "
                f"comment={self.comment}, codec={self.codec}, "
                f"duration={self.duration})")
