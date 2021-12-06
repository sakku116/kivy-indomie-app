# -*- mode: python ; coding: utf-8 -*-
# package aplikasi menjadi standalone+onfile dengan 
# membundle beberapa directory yang dibutuhkan

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

# tambahkan project path string kedalam paramater tree
# seperti
# 'D:\\Ky Project\\coding-project\\Python\\Kivy\\Slicing\\Indomie-App-dev\\'
# dan ubah parameter name menjadi nama aplikasi yang dinginkan

exe = EXE(pyz, Tree('D:\\Ky Project\\coding-project\\Python\\Kivy\\Slicing\\Indomie-App-dev2\\'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          [],
          name='preview',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

'''
dalam file main.py tambahkan beberapa kode

import os, sys
from kivy.resources import resource_add_path, resource_find

dan 

if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))

didalam if __name__ == '__main__':
'''
