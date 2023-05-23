@echo off

cd /d "%~dp0"
call venv\Scripts\activate.bat
python okseg-GUI.py
call deactivate.bat

exit