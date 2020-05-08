@echo off
if exist %~dp0\vrc_meta_reader.exe (
  %~dp0\vrc_meta_reader.exe
) else (
  where /Q python && python %~dp0\vrc_meta_reader.py %1
)
echo.
pause