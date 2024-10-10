@echo off

python -m PyInstaller --noconfirm --onefile --console --name "PyEventbriteScraper" --distpath "." "src/main.py"

del PyEventbriteScraper.spec
rmdir /s /q build