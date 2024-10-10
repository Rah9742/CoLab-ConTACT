@echo off

python -m PyInstaller --noconfirm --onefile --console --name "PyMTCScraper" --distpath "." "src/main.py"

del PyMTCScraper.spec
rmdir /s /q build