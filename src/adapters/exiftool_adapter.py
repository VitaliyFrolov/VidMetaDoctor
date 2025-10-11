import json
import os
import shutil
import subprocess
from typing import Optional

from core.models import VideoMetadata
from utils.constants import SUPPORTED_EXTENSIONS

def _find_exiftool() -> str:
    """
    Возвращает путь к exiftool: сначала локальный resources, потом системный 'exiftool'.
    """
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/exiftool"))
    # mac/linux: 'exiftool', windows: 'exiftool.exe'
    candidates = [
        os.path.join(base, "exiftool"),
        os.path.join(base, "exiftool.exe"),
        "exiftool"
    ]
    for c in candidates:
        if shutil.which(c) or os.path.exists(c):
            return c
    # fallback to 'exiftool' (shutil.which will be None if not found)
    return "exiftool"

def read_metadata(path: str) -> Optional[VideoMetadata]:
    """
    Читает метаданные через exiftool и возвращает VideoMetadata.
    Возвращает None в случае ошибки.
    """
    try:
        exiftool = _find_exiftool()
        # exiftool -j file  -> json output (list)
        proc = subprocess.run([exiftool, "-j", path], capture_output=True, text=True, check=True)
        arr = json.loads(proc.stdout)
        if not arr:
            return None
        info = arr[0]

        title = info.get("Title") or info.get("title") or info.get("TrackTitle") or info.get("Name")
        artist = info.get("Artist") or info.get("Author") or info.get("AuthorName")
        comment = info.get("Comment") or info.get("Description") or info.get("Caption-Abstract")
       
        duration = None
        if "Duration" in info:
            try:
                duration = float(info["Duration"])
            except Exception:
                duration = None

        codec = info.get("VideoCodec") or info.get("CodecID") or info.get("VideoCodecID")

        return VideoMetadata(
            filepath=path,
            title=title,
            artist=artist,
            comment=comment,
            codec=codec,
            duration=duration
        )
    except subprocess.CalledProcessError as e:
        print("exiftool error:", e)
        return None
    except Exception as e:
        print("read_metadata exception:", e)
        return None
