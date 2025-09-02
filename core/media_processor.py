# -*- coding: utf-8 -*-
"""
معالج الوسائط الأساسي
يحتوي على منطق تقطيع الملفات الصوتية والمرئية باستخدام FFmpeg
"""

import os
import subprocess
import threading
import time
import re
from typing import Optional, Callable, Dict, List, Tuple
from datetime import timedelta

class MediaProcessor:
    """فئة معالج الوسائط"""
    
    def __init__(self, config):
        """تهيئة معالج الوسائط"""
        self.config = config
        self.current_process = None
        self.is_processing = False
        self.should_stop = False
        self.progress_callback = None
        self.completion_callback = None
        
    def set_progress_callback(self, callback: Callable[[float, str], None]):
        """تعيين دالة استدعاء لتحديث التقدم"""
        self.progress_callback = callback
    
    def set_completion_callback(self, callback: Callable[[bool, str, str], None]):
        """تعيين دالة استدعاء لإشعار الإنجاز"""
        self.completion_callback = callback
    
    def get_media_info(self, file_path: str) -> Optional[Dict]:
        """الحصول على معلومات الملف الوسائطي"""
        try:
            # التحقق من وجود الملف
            if not os.path.exists(file_path):
                return None
            
            # تشغيل ffprobe للحصول على المعلومات
            cmd = [
                self.config.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                
                # استخراج المعلومات المهمة
                format_info = info.get('format', {})
                duration = float(format_info.get('duration', 0))
                
                # البحث عن تدفق الفيديو والصوت
                video_stream = None
                audio_stream = None
                
                for stream in info.get('streams', []):
                    if stream.get('codec_type') == 'video' and not video_stream:
                        video_stream = stream
                    elif stream.get('codec_type') == 'audio' and not audio_stream:
                        audio_stream = stream
                
                return {
                    'duration': duration,
                    'duration_str': str(timedelta(seconds=int(duration))),
                    'format_name': format_info.get('format_name', ''),
                    'size': int(format_info.get('size', 0)),
                    'bitrate': int(format_info.get('bit_rate', 0)),
                    'video_stream': video_stream,
                    'audio_stream': audio_stream,
                    'is_video': video_stream is not None,
                    'is_audio': audio_stream is not None
                }
            
            return None
            
        except Exception as e:
            print(f"خطأ في الحصول على معلومات الملف: {e}")
            return None
    
    def calculate_segments(self, total_duration: float, segment_duration: float) -> List[Tuple[float, float]]:
        """حساب قطع التقسيم"""
        segments = []
        current_start = 0.0
        
        while current_start < total_duration:
            segment_end = min(current_start + segment_duration * 60, total_duration)
            segments.append((current_start, segment_end))
            current_start = segment_end
            
            if segment_end >= total_duration:
                break
        
        return segments
    
    def format_time(self, seconds: float) -> str:
        """تنسيق الوقت بصيغة HH:MM:SS.mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def generate_output_filename(self, input_file: str, output_dir: str, 
                                part_number: int, output_format: str) -> str:
        """توليد اسم ملف الإخراج"""
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        extension = self.config.get_output_formats_for_file(input_file).get(
            output_format, {}
        ).get('extension', output_format)
        
        filename = f"{base_name}_part_{part_number:02d}.{extension}"
        return os.path.join(output_dir, filename)
    
    def create_output_directory(self, input_file: str, output_format: str, custom_dir: str = None) -> str:
        """إنشاء مجلد الإخراج باستخدام النظام الجديد"""
        # استخدام النظام الجديد من config
        output_dir = self.config.get_output_directory(input_file, output_format, custom_dir)
        
        # إنشاء المجلد إذا لم يكن موجود
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def analyze_media_streams(self, file_path: str) -> Dict:
        """تحليل مسارات الملف الوسائطي"""
        try:
            cmd = [
                self.config.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                streams_info = {
                    'video_streams': [],
                    'audio_streams': [],
                    'subtitle_streams': [],
                    'total_streams': 0
                }
                
                for i, stream in enumerate(data.get('streams', [])):
                    codec_type = stream.get('codec_type', '').lower()
                    
                    if codec_type == 'video':
                        streams_info['video_streams'].append({
                            'index': i,
                            'codec_name': stream.get('codec_name', 'unknown'),
                            'width': stream.get('width', 0),
                            'height': stream.get('height', 0),
                            'fps': stream.get('r_frame_rate', '0/1')
                        })
                    elif codec_type == 'audio':
                        streams_info['audio_streams'].append({
                            'index': i,
                            'codec_name': stream.get('codec_name', 'unknown'),
                            'channels': stream.get('channels', 0),
                            'sample_rate': stream.get('sample_rate', 0),
                            'language': stream.get('tags', {}).get('language', 'unknown')
                        })
                    elif codec_type == 'subtitle':
                        streams_info['subtitle_streams'].append({
                            'index': i,
                            'codec_name': stream.get('codec_name', 'unknown'),
                            'language': stream.get('tags', {}).get('language', 'unknown')
                        })
                
                streams_info['total_streams'] = len(data.get('streams', []))
                return streams_info
                
        except Exception as e:
            print(f"خطأ في تحليل المسارات: {e}")
        
        return {'video_streams': [], 'audio_streams': [], 'subtitle_streams': [], 'total_streams': 0}
    
    def build_ffmpeg_command(self, input_file: str, output_file: str, 
                           start_time: float, duration: float, 
                           output_format: str) -> List[str]:
        """بناء أمر FFmpeg محسن للحفاظ على جميع المسارات"""
        
        # تحليل مسارات الملف أولاً
        streams_info = self.analyze_media_streams(input_file)
        
        cmd = [
            self.config.ffmpeg_path,
            '-i', input_file,
            '-ss', self.format_time(start_time),
            '-t', self.format_time(duration)
        ]
        
        # إضافة معاملات الخريطة بناءً على المسارات الموجودة
        if streams_info['video_streams']:
            # تضمين جميع مسارات الفيديو
            for video_stream in streams_info['video_streams']:
                cmd.extend(['-map', f"0:{video_stream['index']}"])
        
        if streams_info['audio_streams']:
            # تضمين جميع مسارات الصوت
            for audio_stream in streams_info['audio_streams']:
                cmd.extend(['-map', f"0:{audio_stream['index']}"])
        
        if streams_info['subtitle_streams']:
            # تضمين جميع مسارات الترجمة
            for subtitle_stream in streams_info['subtitle_streams']:
                cmd.extend(['-map', f"0:{subtitle_stream['index']}"])
        
        # إعدادات الترميز
        cmd.extend([
            # نسخ جميع أنواع المسارات بدون إعادة ترميز
            '-c', 'copy',
            
            # معالجة الطوابع الزمنية
            '-avoid_negative_ts', 'make_zero',
            
            # تحسينات للتشغيل
            '-movflags', '+faststart',
            
            # نسخ البيانات الوصفية
            '-map_metadata', '0',
            
            # تعيين الترتيب الافتراضي
            '-disposition:v', 'default',
            '-disposition:a', 'default'
        ])
        
        # إضافة معاملات خاصة بالصيغة
        if output_format.lower() == 'mp4':
            cmd.extend(['-movflags', 'faststart'])
        elif output_format.lower() == 'mkv':
            cmd.extend(['-strict', '-2'])
        
        # استبدال الملفات الموجودة والملف الناتج
        cmd.extend(['-y', output_file])
        
        return cmd
    
    def process_media_file(self, input_file: str, segment_duration: float,
                          output_format: str, output_directory: str = None) -> bool:
        """تقطيع الملف الوسائطي"""
        try:
            self.is_processing = True
            self.should_stop = False
            
            # الحصول على معلومات الملف
            media_info = self.get_media_info(input_file)
            if not media_info:
                self._notify_completion(False, "فشل في قراءة معلومات الملف", "")
                return False
            
            total_duration = media_info['duration']
            if total_duration <= 0:
                self._notify_completion(False, "مدة الملف غير صحيحة", "")
                return False
            
            # حساب القطع
            segments = self.calculate_segments(total_duration, segment_duration)
            if not segments:
                self._notify_completion(False, "فشل في حساب قطع التقسيم", "")
                return False
            
            # إنشاء مجلد الإخراج
            output_dir = self.create_output_directory(input_file, output_format, output_directory)
            
            # تحليل مسارات الملف لعرض المعلومات
            streams_info = self.analyze_media_streams(input_file)
            video_count = len(streams_info['video_streams'])
            audio_count = len(streams_info['audio_streams'])
            subtitle_count = len(streams_info['subtitle_streams'])
            
            # إعلام المستخدم بتفاصيل المسارات
            streams_msg = f"سيتم تقطيع الملف مع الاحتفاظ بـ: {video_count} فيديو، {audio_count} صوت"
            if subtitle_count > 0:
                streams_msg += f"، {subtitle_count} ترجمة"
            self._update_progress(5, streams_msg)
            
            # تقطيع الملف مع تحديثات تقدم محسنة
            total_segments = len(segments)
            self._update_progress(5, f"بدء تقطيع الملف إلى {total_segments} أجزاء...")
            
            for i, (start_time, end_time) in enumerate(segments):
                if self.should_stop:
                    self._notify_completion(False, "تم إيقاف العملية بواسطة المستخدم", "")
                    return False
                
                # تحديث التقدم - بداية معالجة الجزء
                base_progress = (i / total_segments) * 90  # 90% للمعالجة، 10% للتهيئة والنهاية
                self._update_progress(base_progress + 5, f"إعداد الجزء {i + 1} من {total_segments}")
                time.sleep(0.3)  # وقت أطول لإظهار التحديث
                
                # توليد اسم الملف
                output_file = self.generate_output_filename(
                    input_file, output_dir, i + 1, output_format
                )
                
                # بناء أمر FFmpeg
                segment_duration_actual = end_time - start_time
                cmd = self.build_ffmpeg_command(
                    input_file, output_file, start_time, segment_duration_actual, output_format
                )
                
                # تحديث التقدم - بدء المعالجة
                self._update_progress(base_progress + 10, f"معالجة الجزء {i + 1} من {total_segments}")
                time.sleep(0.2)  # وقت لإظهار بداية المعالجة
                
                # تنفيذ الأمر
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    encoding='utf-8'
                )
                
                if result.returncode != 0:
                    error_msg = f"فشل في معالجة الجزء {i + 1}: {result.stderr}"
                    self._notify_completion(False, error_msg, "")
                    return False
                
                # تحديث التقدم - إنجاز الجزء
                completed_progress = ((i + 1) / total_segments) * 90 + 5
                self._update_progress(completed_progress, f"تم إنجاز الجزء {i + 1} من {total_segments}")
                time.sleep(0.2)  # وقت لإظهار إنجاز الجزء
            
            # تحديث التقدم النهائي
            self._update_progress(95, "جاري حفظ الملفات النهائية...")
            time.sleep(0.5)  # وقت قصير للحفظ
            
            self._update_progress(100, f"تم إنجاز التقطيع بنجاح - {total_segments} أجزاء")
            self._notify_completion(True, f"تم تقطيع الملف إلى {total_segments} أجزاء بنجاح", output_dir)
            
            return True
            
        except Exception as e:
            error_msg = f"خطأ أثناء معالجة الملف: {str(e)}"
            self._notify_completion(False, error_msg, "")
            return False
        
        finally:
            self.is_processing = False
            self.current_process = None
    
    def process_media_file_async(self, input_file: str, segment_duration: float,
                                output_format: str, output_directory: str = None):
        """تقطيع الملف بشكل غير متزامن"""
        if self.is_processing:
            return False
        
        # تشغيل المعالجة في خيط منفصل
        processing_thread = threading.Thread(
            target=self.process_media_file,
            args=(input_file, segment_duration, output_format, output_directory),
            daemon=True
        )
        processing_thread.start()
        return True
    
    def stop_processing(self):
        """إيقاف المعالجة الحالية"""
        self.should_stop = True
        if self.current_process:
            try:
                self.current_process.terminate()
            except:
                pass
    
    def _update_progress(self, percentage: float, message: str):
        """تحديث التقدم الداخلي"""
        if self.progress_callback:
            self.progress_callback(percentage, message)
    
    def _notify_completion(self, success: bool, message: str, output_path: str):
        """إشعار الإنجاز الداخلي"""
        if self.completion_callback:
            self.completion_callback(success, message, output_path)