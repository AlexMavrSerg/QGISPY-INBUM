# -*- mode: python ; coding: utf-8 -*-
import pkgutil

import rasterio

# list all rasterio and fiona submodules, to include them in the package
additional_packages = list()
for package in pkgutil.iter_modules(rasterio.__path__, prefix="rasterio."):
    additional_packages.append(package.name)
additional_packages.append('tkinter')
additional_packages.append('ttkbootstrap')
additional_packages.append('matplotlib')
additional_packages.append('functools')
additional_packages.append('rasterstats')
additional_packages.append('pandas')
additional_packages.append('numpy')

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=additional_packages,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QGISPY-INBUM-v2-0.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='C:\\Users\\Intel Core I9\\Desktop\\QGISPY\\_new_v2\\inbum.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QGISPY-INBUM-v2-0.1',
)
