@echo off

cd /d "%~dp0"
call venv\Scripts\activate.bat
python .\utils\utils_unitcalc.py
python predict.py
call deactivate.bat

exit