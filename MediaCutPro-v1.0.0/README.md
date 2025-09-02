# 🎬 Media Cut Pro

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**Media Cut Pro** is a professional desktop application for splitting video and audio files into smaller segments. Built with Python and Tkinter, it provides an intuitive interface with advanced features for media processing.

---

## ✨ Features

### 🔥 Core Features
- **Smart File Splitting** - Split any video/audio file into equal time segments
- **Format Preservation** - Maintains original quality and format
- **Stream Conservation** - Preserves all video, audio, and subtitle streams
- **Intelligent Naming** - Auto-generates organized output filenames
- **Progress Tracking** - Real-time progress monitoring with detailed feedback

### 🎯 Advanced Features
- **Multiple Format Support** - MP4, AVI, MKV, MP3, WAV, and more
- **Custom Output Directory** - Choose where to save split files
- **Animated UI** - Smooth Braille spinner animations during processing
- **Error Handling** - Comprehensive error detection and reporting
- **FFmpeg Integration** - Powerful media processing engine included

---

## 🚀 Quick Start

### Method 1: Run from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/media-cut-pro.git
cd media-cut-pro

# Run the application
python app.py
```

### Method 2: Download Executable
1. Download the latest release from [Releases](https://github.com/yourusername/media-cut-pro/releases)
2. Extract the ZIP file
3. Run `MediaCutPro.exe`

---

## 🛠️ Installation

### Prerequisites
- **Python 3.8+** (for source version)
- **Windows 10/11** (recommended)
- **250MB free space** (for executable version)

### From Source
```bash
# Clone repository
git clone https://github.com/yourusername/media-cut-pro.git
cd media-cut-pro

# Install dependencies (optional)
pip install -r requirements.txt

# Run application
python app.py
```

---

## 📋 Usage Guide

### Step 1: Select Input File
1. Click **"Choose File"** button
2. Browse and select your video/audio file
3. Supported formats: MP4, AVI, MKV, MOV, MP3, WAV, AAC, and more

### Step 2: Configure Settings
1. **Duration**: Set segment length in minutes (1-60)
2. **Format**: Choose output format (auto-detected from input)
3. **Output Directory**: Select where to save split files (optional)

### Step 3: Start Processing
1. Click **"Start Splitting"** button
2. Watch real-time progress with animated spinner ⠋
3. Files are automatically organized in output folder

### Step 4: Access Results
1. Click **"Open Output"** when complete
2. Find organized files in timestamped folders
3. Each segment maintains original quality and metadata

---

## 🏗️ Project Structure

```
media-cut-pro/
├── 📄 app.py                    # Main application entry point
├── 📁 ui/                       # User interface components
│   └── main_window.py          # Main window implementation
├── 📁 core/                     # Core processing logic
│   └── media_processor.py      # Media splitting engine
├── 📁 config/                   # Configuration management
│   └── settings.py             # App settings and formats
├── 📁 ffmpeg/                   # FFmpeg binaries (included)
│   ├── ffmpeg.exe
│   └── ffprobe.exe
├── 📄 requirements.txt          # Python dependencies
├── 📄 build.py                  # Build script for executable
└── 📄 README.md                 # This file
```

---

## 🎥 Supported Formats

### Video Formats
- **MP4** - MPEG-4 Video
- **AVI** - Audio Video Interleave
- **MKV** - Matroska Video
- **MOV** - QuickTime Movie
- **WMV** - Windows Media Video
- **FLV** - Flash Video
- **WebM** - WebM Video

### Audio Formats
- **MP3** - MPEG Audio Layer 3
- **WAV** - Waveform Audio File
- **AAC** - Advanced Audio Coding
- **FLAC** - Free Lossless Audio Codec
- **OGG** - Ogg Vorbis
- **M4A** - MPEG-4 Audio

---

## 🔧 Building from Source

### Prerequisites for Building
```bash
pip install pyinstaller
```

### Build Executable
```bash
python build.py
```

This will create a standalone executable in the `dist/` directory.

---

## 🐛 Troubleshooting

### Common Issues
- **Application won't start**: Run as administrator
- **Unsupported file**: Check if format is supported
- **Low disk space**: Ensure sufficient space available
- **Slow processing**: Large files require more time

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and release notes
- **Email**: Contact developer for support

---

## 📈 Performance

### Benchmarks
- **1GB file**: Split in ~2-3 minutes
- **500MB file**: Split in ~1-2 minutes
- **Memory usage**: 40-60MB during processing
- **CPU usage**: Moderate, depends on file size

### Optimizations
- **Parallel processing**: Multi-threaded operations
- **Memory efficient**: Smart memory management
- **Chunked reading**: Efficient large file handling

---

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/media-cut-pro.git
cd media-cut-pro

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Drikon** - *Project Creator & Lead Developer*

---

## 🙏 Acknowledgments

- **FFmpeg Team** for the powerful media processing library
- **Python Community** for excellent documentation and support
- **Tkinter** for the reliable GUI framework

---

## 🔄 Roadmap

### v1.1.0 (Coming Soon)
- Advanced splitting with custom time points
- Enhanced quality settings
- Separate subtitle support
- English interface option

### v1.2.0 (Planned)
- File preview functionality
- Basic editing features
- Batch processing support
- Export templates

---

**⭐ Star this repository if you find it helpful!**

For questions, suggestions, or support, please open an issue on GitHub.