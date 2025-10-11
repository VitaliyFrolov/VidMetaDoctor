import os
import shutil
from pathlib import Path

def get_resource_path(*parts):
    """
    Возвращает абсолютный путь к ресурсу проекта (resources/...), кроссплатформенно.
    Использует __file__ для вычисления корня src/.
    """
    base_dir = Path(__file__).parent.parent  # src/
    return str(base_dir / "resources" / Path(*parts))

def find_executable(candidates):
    """
    Ищет первый существующий исполняемый файл в списке candidates или в PATH.
    Возвращает путь к найденному файлу, либо None.
    """
    for c in candidates:
        if os.path.exists(c) and os.access(c, os.X_OK):
            return c
        path_in_system = shutil.which(c)
        if path_in_system:
            return path_in_system
    return None

def backup_file(file_path, backup_dir=None):
    """
    Создаёт копию файла в backup_dir. Если backup_dir=None, создаёт рядом с оригиналом с суффиксом .bak
    """
    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)
        target = os.path.join(backup_dir, os.path.basename(file_path))
    else:
        target = file_path + ".bak"
    shutil.copy2(file_path, target)
    return target

def is_supported_extension(file_path, supported_extensions):
    """
    Проверяет, что расширение файла в списке supported_extensions
    """
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    return ext in supported_extensions
