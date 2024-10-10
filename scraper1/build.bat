@echo off

python -m PyInstaller --noconfirm --onefile --console --name "PyUniScraper" --distpath "." "src/main.py"

del PyUniScraper.spec
rmdir /s /q build