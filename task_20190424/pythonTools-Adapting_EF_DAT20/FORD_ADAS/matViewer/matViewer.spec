# -*- mode: python -*-

block_cipher = None


a = Analysis(['matViewer.py'],
             pathex=['C:\\Users\\wj5y0m\\Documents\\PythonScripts\\git_python\\matViewer\\src'],
             binaries=None,
             datas=None,
             hiddenimports=['matplotlib.pyplot', 'FixTk', 'Tkinter', 'scipy.linalg', 'scipy.linalg.cython_blas', 'scipy.linalg.cython_lapack', 'scipy.integrate', 'h5py._errors', 'h5py.defs', 'h5py.utils', 'h5py.h5ac', 'h5py._proxy', 'tkinter.filedialog'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='matViewer',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='res\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='matViewer')
