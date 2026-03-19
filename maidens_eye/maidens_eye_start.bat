@echo off
cd /d "%~dp0"
pyw -3 app.py
if errorlevel 1 (
  start py -3 app.py
)
