@echo off

cd /d "%~dp0"
call venv\Scripts\activate.bat
python .\utils\utils_unitcalc.py
python okseg-GUI.py
call deactivate.bat

exit