@echo off
REM 打开浏览器（有头模式）访问去哪儿机票页 - 由会话自动生成
"%~dp0..\.venv\Scripts\playwright.exe" open --channel chrome https://flight.qunar.com/
