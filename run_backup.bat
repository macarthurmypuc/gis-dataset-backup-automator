@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python.exe -m src.main