# -*- coding: utf-8 -*-
"""
إعدادات وتكوين التطبيق
يحتوي على جميع الإعدادات العامة والثوابت المستخدمة في التطبيق
"""

import os
from typing import Dict, Any, List, Tuple

class AppConfig:
    """فئة إعدادات التطبيق"""
    
    def __init__(self):
        """تهيئة الإعدادات"""
        self.setup_paths()
        self.setup_media_formats()
        self.setup_ui_settings()
        self.setup_processing_settings()
    
    def setup_paths(self):
        """إعداد المسارات"""
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ffmpeg_path = os.path.join(self.project_root, "ffmpeg", "ffmpeg.exe")
        self.ffprobe_path = os.path.join(self.project_root, "ffmpeg", "ffprobe.exe")
        self.assets_path = os.path.join(self.project_root, "assets")
        self.temp_path = os.path.join(self.project_root, "temp")
    
    def setup_media_formats(self):
        """إعداد صيغ الوسائط المدعومة"""
        # صيغ الفيديو المدعومة
        self.video_input_formats = {
            'mp4': 'MPEG-4 Video',
            'mkv': 'Matroska Video',
            'mov': 'QuickTime Movie',
            'avi': 'Audio Video Interleave',
            'wmv': 'Windows Media Video',
            'flv': 'Flash Video',
            'webm': 'WebM Video',
            'm4v': 'MPEG-4 Video'
        }
        
        # صيغ الصوت المدعومة
        self.audio_input_formats = {
            'mp3': 'MPEG Audio Layer 3',
            'wav': 'Waveform Audio',
            'flac': 'Free Lossless Audio Codec',
            'aac': 'Advanced Audio Coding',
            'ogg': 'Ogg Vorbis',
            'wma': 'Windows Media Audio',
            'm4a': 'MPEG-4 Audio'
        }
        
        # صيغ الإخراج للفيديو
        self.video_output_formats = {
            'mp4': {'extension': 'mp4', 'codec': 'libx264', 'description': 'MP4 (H.264)'},
            'mkv': {'extension': 'mkv', 'codec': 'libx264', 'description': 'MKV (H.264)'},
            'mov': {'extension': 'mov', 'codec': 'libx264', 'description': 'MOV (H.264)'},
            'avi': {'extension': 'avi', 'codec': 'libx264', 'description': 'AVI (H.264)'}
        }
        
        # صيغ الإخراج للصوت
        self.audio_output_formats = {
            'mp3': {'extension': 'mp3', 'codec': 'libmp3lame', 'description': 'MP3'},
            'wav': {'extension': 'wav', 'codec': 'pcm_s16le', 'description': 'WAV'},
            'flac': {'extension': 'flac', 'codec': 'flac', 'description': 'FLAC'},
            'aac': {'extension': 'aac', 'codec': 'aac', 'description': 'AAC'}
        }
        
        # تجميع جميع الصيغ المدعومة
        self.all_input_formats = {**self.video_input_formats, **self.audio_input_formats}
    
    def setup_ui_settings(self):
        """إعداد واجهة المستخدم"""
        # ألوان التطبيق
        self.colors = {
            'primary': '#2c3e50',      # أزرق داكن
            'secondary': '#3498db',    # أزرق فاتح
            'success': '#27ae60',      # أخضر
            'warning': '#f39c12',      # برتقالي
            'danger': '#e74c3c',       # أحمر
            'light': '#ecf0f1',        # رمادي فاتح
            'dark': '#34495e'          # رمادي داكن
        }
        
        # خطوط التطبيق
        self.fonts = {
            'default': ('Segoe UI', 10),
            'title': ('Segoe UI', 14, 'bold'),
            'button': ('Segoe UI', 10),
            'small': ('Segoe UI', 8)
        }
        
        # إعدادات النافذة
        self.window_settings = {
            'min_width': 600,
            'min_height': 350,      # تقليل أكثر من 400 إلى 350
            'default_width': 650,
            'default_height': 370,  # تقليل أكثر من 420 إلى 370
            'max_width': 800,
            'max_height': 500       # تقليل أكثر من 550 إلى 500
        }
    
    def setup_processing_settings(self):
        """إعدادات المعالجة"""
        # إعدادات التقطيع الافتراضية
        self.default_split_duration = 10  # بالدقائق
        self.min_split_duration = 1       # أقل مدة للتقطيع (دقيقة)
        self.max_split_duration = 120     # أقصى مدة للتقطيع (ساعتين)
        
        # إعدادات جودة الفيديو
        self.video_quality_presets = {
            'high': {'crf': '18', 'preset': 'medium'},
            'medium': {'crf': '23', 'preset': 'medium'},
            'low': {'crf': '28', 'preset': 'fast'}
        }
        
        # إعدادات جودة الصوت
        self.audio_quality_presets = {
            'high': {'bitrate': '320k'},
            'medium': {'bitrate': '192k'},
            'low': {'bitrate': '128k'}
        }
        
        # إعدادات المعالجة
        self.processing_settings = {
            'max_concurrent_processes': 1,  # عدد العمليات المتزامنة
            'temp_cleanup': True,           # تنظيف الملفات المؤقتة
            'overwrite_existing': False,    # استبدال الملفات الموجودة
            'create_named_folders': True,   # إنشاء مجلدات بأسماء الملفات
            'include_format_in_name': True  # تضمين صيغة الإخراج في اسم المجلد
        }
    
    def get_file_filter_string(self) -> str:
        """إرجاع نص فلتر الملفات للحوار"""
        video_extensions = ';'.join([f'*.{ext}' for ext in self.video_input_formats.keys()])
        audio_extensions = ';'.join([f'*.{ext}' for ext in self.audio_input_formats.keys()])
        all_extensions = ';'.join([f'*.{ext}' for ext in self.all_input_formats.keys()])
        
        return (
            f"جميع الملفات المدعومة|{all_extensions}|"
            f"ملفات الفيديو|{video_extensions}|"
            f"ملفات الصوت|{audio_extensions}|"
            f"جميع الملفات|*.*"
        )
    
    def is_video_file(self, file_path: str) -> bool:
        """التحقق من كون الملف فيديو"""
        if not file_path:
            return False
        extension = file_path.lower().split('.')[-1] if '.' in file_path else ''
        return extension in self.video_input_formats
    
    def is_audio_file(self, file_path: str) -> bool:
        """التحقق من كون الملف صوتي"""
        if not file_path:
            return False
        extension = file_path.lower().split('.')[-1] if '.' in file_path else ''
        return extension in self.audio_input_formats
    
    def get_output_formats_for_file(self, file_path: str) -> Dict[str, Dict[str, str]]:
        """الحصول على صيغ الإخراج المناسبة للملف"""
        if self.is_video_file(file_path):
            return self.video_output_formats
        elif self.is_audio_file(file_path):
            return self.audio_output_formats
        else:
            return {}
    
    def validate_ffmpeg_installation(self) -> Tuple[bool, str]:
        """التحقق من وجود FFmpeg"""
        if not os.path.exists(self.ffmpeg_path):
            return False, f"لم يتم العثور على FFmpeg في: {self.ffmpeg_path}"
        
        if not os.path.exists(self.ffprobe_path):
            return False, f"لم يتم العثور على FFprobe في: {self.ffprobe_path}"
        
        return True, "تم العثور على FFmpeg بنجاح"
    
    def create_output_folder_name(self, input_file_path: str, output_format: str) -> str:
        """إنشاء اسم مجلد الإخراج بناءً على اسم الملف والصيغة"""
        # استخراج اسم الملف بدون المسار والامتداد
        file_name = os.path.splitext(os.path.basename(input_file_path))[0]
        
        # تنظيف اسم الملف من الأحرف غير المقبولة
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            file_name = file_name.replace(char, '_')
        
        # إنشاء اسم المجلد
        if self.processing_settings.get('include_format_in_name', True):
            folder_name = f"{file_name}_{output_format.upper()}_segments"
        else:
            folder_name = f"{file_name}_segments"
        
        return folder_name
    
    def get_output_directory(self, input_file_path: str, output_format: str, custom_output_dir: str = None) -> str:
        """الحصول على مجلد الإخراج الكامل"""
        folder_name = self.create_output_folder_name(input_file_path, output_format)
        
        if custom_output_dir and os.path.exists(custom_output_dir):
            # استخدام المجلد المحدد من المستخدم
            output_path = os.path.join(custom_output_dir, folder_name)
        else:
            # استخدام نفس مجلد الملف الأصلي
            input_dir = os.path.dirname(input_file_path)
            output_path = os.path.join(input_dir, folder_name)
        
        return output_path

# إنشاء مثيل عام للإعدادات
app_config = AppConfig()