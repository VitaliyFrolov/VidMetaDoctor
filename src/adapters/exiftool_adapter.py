import os
import sys
import shutil
import subprocess
import json
from typing import Optional

from core.models import VideoMetadata
from utils.constants import SUPPORTED_EXTENSIONS

# ----------------------
# PRIVATE HELPERS
# ----------------------

def _find_exiftool() -> str:
    """
    Возвращает путь к exiftool:
    - сначала локальный resources/exiftool
    - потом системный 'exiftool'
    """
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/exiftool"))

    candidates = []
    if sys.platform.startswith("darwin"):  # macOS
        candidates.append(os.path.join(base, "mac/exiftool"))
    elif sys.platform.startswith("win"):  # Windows
        candidates.append(os.path.join(base, "win/exiftool.exe"))
    else:  # Linux/Other
        candidates.append(os.path.join(base, "linux/exiftool"))

    candidates.append("exiftool")  # fallback

    for c in candidates:
        if shutil.which(c) or os.path.exists(c):
            return c
    return "exiftool"


def _run_exiftool(args: list[str]) -> Optional[list[dict]]:
    """
    Запускает exiftool с аргументами и возвращает результат как список словарей.
    """
    exiftool = _find_exiftool()
    try:
        proc = subprocess.run([exiftool] + args, capture_output=True, text=True, check=True)
        output = proc.stdout
        return json.loads(output)
    except subprocess.CalledProcessError as e:
        print("ExifTool error:", e)
        return None
    except Exception as e:
        print("Exception in _run_exiftool:", e)
        return None


def _parse_duration(value: str) -> float:
    """Парсит Duration из ExifTool в секунды."""
    if not value:
        return 0.0
    value = value.strip()
    # пример: '6.93 s'
    if value.endswith("s"):
        try:
            return float(value[:-1])
        except ValueError:
            return 0.0
    # пример: '00:01:23'
    parts = value.split(":")
    try:
        parts = [float(p) for p in parts]
        if len(parts) == 3:  # hh:mm:ss
            return parts[0]*3600 + parts[1]*60 + parts[2]
        elif len(parts) == 2:  # mm:ss
            return parts[0]*60 + parts[1]
        elif len(parts) == 1:  # ss
            return parts[0]
    except ValueError:
        return 0.0
    return 0.0

# ----------------------
# PUBLIC API
# ----------------------

def read_metadata(file_path: str) -> Optional[VideoMetadata]:
    """
    Читает метаданные видео через exiftool и возвращает VideoMetadata.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    result = _run_exiftool(["-j", file_path])
    if not result:
        return None

    info = result[0]
    duration_raw = info.get("Duration", "")
    return VideoMetadata(
        filepath=file_path,
        title=info.get("Title") or info.get("TrackTitle") or info.get("Name") or "",
        artist=info.get("Artist") or info.get("Author") or info.get("AuthorName") or "",
        comment=info.get("Comment") or info.get("Description") or info.get("Caption-Abstract") or "",
        codec=info.get("VideoCodec") or info.get("CodecID") or info.get("VideoCodecID") or "",
        duration=_parse_duration(duration_raw)
    )


def write_metadata(file_path: str, metadata: VideoMetadata, keep_backup: bool = True) -> bool:
    """
    Записывает метаданные видео через exiftool.
    Если keep_backup=True, создаёт резервную копию с расширением "_original".
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    args = ["-j=-"]
    if not keep_backup:
        args.append("-overwrite_original")

    meta_dict = {}
    if metadata.title:
        meta_dict["Title"] = metadata.title
    if metadata.artist:
        meta_dict["Artist"] = metadata.artist
    if metadata.comment:
        meta_dict["Comment"] = metadata.comment

    try:
        exiftool = _find_exiftool()
        proc = subprocess.run(
            [exiftool] + args + [file_path],
            input=json.dumps([meta_dict]),
            text=True,
            capture_output=True,
            check=True
        )
        return proc.returncode == 0
    except subprocess.CalledProcessError as e:
        print("ExifTool write error:", e)
        return False
    except Exception as e:
        print("Exception in write_metadata:", e)
        return False
