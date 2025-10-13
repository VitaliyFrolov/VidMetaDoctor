import sys
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

block_cipher = None

hidden_imports = collect_submodules('PySide6')

qt_plugins = collect_dynamic_libs('PySide6')

a = Analysis(
    ['src/app.py'],
    pathex=['.'],
    binaries=qt_plugins,
    datas=[
        ('resources/exiftool/mac/*', 'resources/exiftool/mac'),
        ('resources/exiftool/linux/*', 'resources/exiftool/linux'),
        ('resources/exiftool/win/*', 'resources/exiftool/win'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VidMetaEdit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
)
