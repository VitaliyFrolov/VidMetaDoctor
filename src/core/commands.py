import os
import shutil
import subprocess
from typing import Optional
from core.models import VideoMetadata


def _find_tool(candidates):
    import shutil
    for c in candidates:
        if shutil.which(c) or os.path.exists(c):
            return c
    return None

def write_metadata_exiftool(file_path: str, metadata: VideoMetadata, keep_backup: bool = True) -> bool:
    """
    Пишем через exiftool. По умолчанию exiftool создаст backup (file_path_original).
    Если keep_backup=False — используем -overwrite_original.
    Возвращаем True/False.
    """
    exif_candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/exiftool/exiftool")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/exiftool/exiftool.exe")),
        "exiftool"
    ]
    exiftool = _find_tool(exif_candidates)
    if not exiftool:
        print("exiftool not found")
        return False

    cmd = [exiftool]
    if not keep_backup:
        cmd.append("-overwrite_original")

    # only include tags that are not None
    if metadata.title is not None:
        cmd.append(f"-Title={metadata.title}")
    if metadata.artist is not None:
        cmd.append(f"-Artist={metadata.artist}")
    if metadata.comment is not None:
        cmd.append(f"-Comment={metadata.comment}")

    # Example: support custom tags via -XMP or other namespaces if needed
    # cmd.append("-XMP:MyTag=Value")

    cmd.append(file_path)

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("exiftool write error:", e)
        return False

def write_metadata_mkvpropedit(file_path: str, metadata: VideoMetadata) -> bool:
    """
    Быстрая правка заголовка контейнера для MKV через mkvpropedit (без перезаписи всего файла).
    Поддерживает только поля, которые mkvpropedit умеет (title).
    """
    mkv = _find_tool(["mkvpropedit", os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/mkvtoolnix/mkvpropedit"))])
    if not mkv:
        print("mkvpropedit not found")
        return False
    
    cmd = [mkv, file_path]
    if metadata.title is not None:
        cmd += ["--set", f"title={metadata.title}"]

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("mkvpropedit error:", e)
        return False
