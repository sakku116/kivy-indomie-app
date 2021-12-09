# -*- mode: python ; coding: utf-8 -*-

'''
PACKAGE APLIKASI MENJADI STANDALONE(onedir) DENGAN 
MEMBUNDLE BEBERAPA DIRECTORY YANG DIBUTUHKAN
====================================================

direkomendasikan melakukan packaging menggunakan python3.8(support win 7).
jika menggunakan 3.9(sudah tidak support win7) 
maka akan terjadi missing "api-ms-win-core-path-l1-1-0.dll" 
(yang hanya support win8 keatas) pada saat dijalankan di win7
====================================================


dalam file main.py tambahkan beberapa kode:
#----------------------------------------------------#
import os, sys
from kivy.resources import resource_add_path, resource_find
#----------------------------------------------------#


dan didalam "if __name__ == '__main__':"
tambahkan:
#----------------------------------------------------#
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
#----------------------------------------------------#


terakhir tinggal jalankan pyinstaller
#------------------------------------#
pyinstaller --workpath "./output/build" --distpath "./output/dist" --clean onedir.spec -y
#------------------------------------#
'''

from kivy_deps import sdl2, glew

block_cipher = None

# ubah parameter datas dengan menambahkan tuple untuk satu directory
# ('dir/*', 'dir/'), ('dir2/*', 'dir/')

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('assets/*', 'assets/'),('uix/*','uix/'),('screens/*','screens/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='preview(onedir)',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

# tambahkan project path string kedalam paramater 'tree'
# seperti
# 'path\\to\\project\\folder\\'
# dan ubah parameter 'name' menjadi nama aplikasi yang dinginkan

coll = COLLECT(exe, Tree('D:\\Ky Project\\coding-project\\Python\\Kivy\\Slicing\\Indomie-App-dev\\'),
               a.binaries,
               a.zipfiles,
               a.datas, 
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='preview(onedir)')
