# mangadex-dl-pyinstaller-bootloader
PyInstaller with custom bootloader for mangadex-downloader

This is to avoid false virus flag from virustotal. mangadex-downloader is compiled using PyInstaller and using PyInstaller default bootloader, so i guess they flagged the bootloader causing the mangadex-downloader is flagged as virus too. 

The bootloader doesn't contain any modification, i just re-compile it.

## Custom bootloader

[![image](https://github.com/user-attachments/assets/c23cfaa9-4ea6-419f-be69-76ebe531bfd6)](https://www.virustotal.com/gui/file/bf594401329ee4927202c7337a1748c31a4daccca09e74d07f9d7f2454698c71?nocache=1)

## Built-in bootloader from PyInstaller

[![image](https://github.com/user-attachments/assets/8d0e4e65-eb38-4290-a9a2-e802d05810d9)](https://www.virustotal.com/gui/file/8943280a34725d114b5dbf2681b6329f7728f77436414772bd43eb941028ed2b/detection)


Reference: https://github.com/mansuf/mangadex-downloader/issues/157
