import PyInstaller.__main__

# requirements:
# pip install -r requirements.txt
# py -m pip install pigar
# # py -m pigar generate


PyInstaller.__main__.run([
    'webp2jpg.py',
    '--onefile',
    # '--icon=icon.ico',
    # '--onedir',
    # '-w'   #als demon = ohne shell
])