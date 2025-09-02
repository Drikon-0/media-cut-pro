@echo off
echo.
echo ========================================
echo   Media Cut Pro v1.0.0 Installer
echo ========================================
echo.
echo Installing Media Cut Pro...

set "INSTALL_DIR=%USERPROFILE%\Desktop\Media Cut Pro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying files...
copy "%~dp0MediaCutPro.exe" "%INSTALL_DIR%\" >nul
copy "%~dp0README.md" "%INSTALL_DIR%\" >nul 2>nul
copy "%~dp0HOW_TO_USE.txt" "%INSTALL_DIR%\" >nul 2>nul

echo Creating desktop shortcut...
set "SHORTCUT=%USERPROFILE%\Desktop\Media Cut Pro.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\MediaCutPro.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\MediaCutPro.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation completed successfully!
echo.
echo Media Cut Pro installed to:
echo %INSTALL_DIR%
echo.
echo Desktop shortcut created.
echo ========================================
echo.
pause
