# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all


# Pastikan semua modul mysql.connector terbawa agar koneksi database
# tetap berfungsi pada hasil bundling onefile.
mysql_datas, mysql_binaries, mysql_hiddenimports = collect_all("mysql.connector")

asset_datas = [('assets', 'assets')]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=mysql_binaries,
    datas=asset_datas + mysql_datas,
    hiddenimports=mysql_hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
