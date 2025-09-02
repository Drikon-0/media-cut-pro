#!/usr/bin/env python3
"""
Media Cut Pro - Build Script
============================

This script creates a standalone executable for Media Cut Pro with embedded FFmpeg binaries.
Uses PyInstaller to package the application with all dependencies.

Author: Drikon
Version: 1.0.0
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Build configuration
APP_NAME = "MediaCutPro"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional Media Splitting Tool"
APP_AUTHOR = "Drikon"

# Paths
PROJECT_ROOT = Path(__file__).parent
APP_SCRIPT = PROJECT_ROOT / "app.py"
ICON_FILE = PROJECT_ROOT / "media cut pro.ico"
FFMPEG_DIR = PROJECT_ROOT / "ffmpeg"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
RELEASE_DIR = PROJECT_ROOT / f"{APP_NAME}-v{APP_VERSION}"

def print_header():
    """Print build script header"""
    print("=" * 60)
    print(f"📦 Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print(f"🎯 Target: Windows Executable")
    print(f"📁 Source: {APP_SCRIPT}")
    print(f"🎨 Icon: {ICON_FILE}")
    print(f"🛠️  Tool: PyInstaller")
    print("-" * 60)

def check_prerequisites():
    """Check if all required files and tools are available"""
    print("🔍 Checking prerequisites...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"], check=True)
        print("✅ PyInstaller installed successfully")
    
    # Check required files
    required_files = [APP_SCRIPT, ICON_FILE]
    for file_path in required_files:
        if file_path.exists():
            print(f"✅ Found: {file_path.name}")
        else:
            print(f"❌ Missing: {file_path}")
            sys.exit(1)
    
    # Check FFmpeg binaries
    ffmpeg_exe = FFMPEG_DIR / "ffmpeg.exe"
    ffprobe_exe = FFMPEG_DIR / "ffprobe.exe"
    
    if ffmpeg_exe.exists() and ffprobe_exe.exists():
        print(f"✅ FFmpeg binaries found in {FFMPEG_DIR}")
    else:
        print(f"❌ Missing FFmpeg binaries in {FFMPEG_DIR}")
        sys.exit(1)
    
    print("✅ All prerequisites satisfied")
    print()

def clean_build_dirs():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = [BUILD_DIR, DIST_DIR, RELEASE_DIR]
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"🗑️  Removed: {dir_path}")
    
    print("✅ Build directories cleaned")
    print()

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # PyInstaller command with enhanced integration
    cmd = [
        "pyinstaller",
        "--onefile",                                    # Single executable file
        "--windowed",                                   # No console window
        "--noconfirm",                                  # Overwrite output without confirmation
        f"--icon={ICON_FILE}",                         # Application icon
        f"--name={APP_NAME}",                          # Executable name
        f"--add-data={FFMPEG_DIR}{os.sep}*;ffmpeg",   # Include ALL FFmpeg files
        f"--add-data={ICON_FILE};.",                   # Include icon file in root
        "--add-data=ui;ui",                            # Include UI module
        "--add-data=core;core",                        # Include core module  
        "--add-data=config;config",                    # Include config module
        "--hidden-import=tkinter",                      # Ensure tkinter is included
        "--hidden-import=tkinter.ttk",                  # Ensure ttk is included
        "--hidden-import=tkinter.filedialog",           # Ensure filedialog is included
        "--hidden-import=tkinter.messagebox",           # Ensure messagebox is included
        "--hidden-import=ui.main_window",               # Include main window
        "--hidden-import=core.media_processor",         # Include media processor
        "--hidden-import=config.settings",              # Include settings
        "--collect-all=tkinter",                        # Collect all tkinter modules
        "--clean",                                      # Clean cache before building
        "--optimize=2",                                 # Optimize bytecode
        "--exclude-module=matplotlib",                  # Exclude unnecessary modules
        "--exclude-module=numpy",                       # Exclude unnecessary modules
        "--exclude-module=scipy",                       # Exclude unnecessary modules
        "--distpath=dist",                             # Output directory
        "--workpath=build",                            # Work directory
        str(APP_SCRIPT)                                # Main script
    ]
    
    # Add version info for Windows
    version_info = f"""
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({APP_VERSION.replace('.', ',')},0),
    prodvers=({APP_VERSION.replace('.', ',')},0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{APP_AUTHOR}'),
        StringStruct(u'FileDescription', u'{APP_DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{APP_VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'© {APP_AUTHOR}'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{APP_VERSION}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    print("🚀 Running PyInstaller...")
    print(f"📝 Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyInstaller completed successfully")
        
        # Show build output
        if result.stdout:
            print("📋 Build output:")
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed with error: {e}")
        if e.stdout:
            print("📋 stdout:", e.stdout)
        if e.stderr:
            print("📋 stderr:", e.stderr)
        sys.exit(1)
    
    print()

def create_release_package():
    """Create a release package with executable and documentation"""
    print("📦 Creating release package...")
    
    # Create release directory
    RELEASE_DIR.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = DIST_DIR / f"{APP_NAME}.exe"
    exe_dest = RELEASE_DIR / f"{APP_NAME}.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ Copied executable: {exe_dest}")
    else:
        print(f"❌ Executable not found: {exe_source}")
        sys.exit(1)
    
    # Copy documentation
    docs_to_copy = ["README.md", "requirements.txt"]
    for doc in docs_to_copy:
        doc_path = PROJECT_ROOT / doc
        if doc_path.exists():
            shutil.copy2(doc_path, RELEASE_DIR / doc)
            print(f"✅ Copied: {doc}")
    
    # Create usage instructions
    usage_file = RELEASE_DIR / "HOW_TO_USE.txt"
    usage_content = f"""
Media Cut Pro v{APP_VERSION} - Usage Instructions
================================================

🚀 Quick Start:
1. Double-click MediaCutPro.exe to start the application
2. Click "Choose File" to select your video/audio file
3. Set the split duration in minutes
4. Choose output format (auto-detected)
5. Click "Start Splitting" to begin processing
6. Use "Open Output" to view results

📋 System Requirements:
- Windows 10 or higher
- At least 4GB RAM
- 500MB free disk space
- Video/audio files to split

🔧 Features:
- Supports MP4, AVI, MKV, MP3, WAV, and many more formats
- Preserves original quality (no re-encoding)
- Smart folder organization with timestamps
- Real-time progress tracking with animations
- Integrated FFmpeg processing engine
- Embedded icon and resources

🐛 Troubleshooting:
- If the app doesn't start, try running as administrator
- For large files, ensure sufficient disk space
- Supported file formats are auto-detected
- All FFmpeg tools are embedded in the executable

📧 Support:
- GitHub: https://github.com/yourusername/media-cut-pro
- Author: {APP_AUTHOR}
- Version: {APP_VERSION}

Thank you for using Media Cut Pro! 🎬
"""
    
    with open(usage_file, 'w', encoding='utf-8') as f:
        f.write(usage_content)
    print(f"✅ Created: {usage_file.name}")
    
    # Get file sizes
    exe_size = exe_dest.stat().st_size / (1024 * 1024)  # MB
    
    print(f"📊 Release package created in: {RELEASE_DIR}")
    print(f"📏 Executable size: {exe_size:.1f} MB")
    print()

def create_installer():
    """Create a simple batch installer"""
    print("📦 Creating installer script...")
    
    installer_script = RELEASE_DIR / "install.bat"
    installer_content = f"""@echo off
echo.
echo ========================================
echo   Media Cut Pro v{APP_VERSION} Installer
echo ========================================
echo.
echo Installing Media Cut Pro...

set "INSTALL_DIR=%USERPROFILE%\\Desktop\\Media Cut Pro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying files...
copy "%~dp0MediaCutPro.exe" "%INSTALL_DIR%\\" >nul
copy "%~dp0README.md" "%INSTALL_DIR%\\" >nul 2>nul
copy "%~dp0HOW_TO_USE.txt" "%INSTALL_DIR%\\" >nul 2>nul

echo Creating desktop shortcut...
set "SHORTCUT=%USERPROFILE%\\Desktop\\Media Cut Pro.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MediaCutPro.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\MediaCutPro.exe'; $Shortcut.Save()"

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
"""
    
    with open(installer_script, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    print(f"✅ Created installer: {installer_script.name}")
    print()

def print_summary():
    """Print build summary"""
    exe_path = RELEASE_DIR / f"{APP_NAME}.exe"
    
    print("=" * 60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📦 Release package: {RELEASE_DIR}")
    print(f"🚀 Executable: {exe_path}")
    print(f"📖 Documentation included")
    print(f"💾 Installer script included")
    print()
    print("📋 Release contents:")
    for item in RELEASE_DIR.iterdir():
        size = item.stat().st_size / 1024  # KB
        print(f"   📄 {item.name} ({size:.1f} KB)")
    print()
    print("🎯 Next steps:")
    print("1. Test the executable by running it")
    print("2. Create a ZIP archive for distribution")
    print("3. Upload to GitHub Releases")
    print("4. Share with users!")
    print()
    print("✨ Ready for distribution! ✨")
    print("=" * 60)

def main():
    """Main build process"""
    try:
        print_header()
        check_prerequisites()
        clean_build_dirs()
        build_executable()
        create_release_package()
        create_installer()
        print_summary()
        
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()