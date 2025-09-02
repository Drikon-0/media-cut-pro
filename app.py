#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Cut Pro - Advanced Media Splitting Application
Main application entry point

Developed by: Python Code Gear-1 with Claude Sonnet
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# إضافة مسار المشروع إلى sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# استيراد الوحدات المحلية
try:
    from ui.main_window import MainWindow
    from config.settings import AppConfig
    from core.media_processor import MediaProcessor
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class MediaCutProApp:
    """الفئة الرئيسية للتطبيق"""
    
    def __init__(self):
        """تهيئة التطبيق"""
        self.root = None
        self.main_window = None
        self.config = None
        self.media_processor = None
        
    def initialize(self):
        """تهيئة مكونات التطبيق"""
        try:
            # تهيئة التكوين
            self.config = AppConfig()
            
            # تهيئة النافذة الرئيسية
            self.root = tk.Tk()
            self.setup_root_window()
            
            # تهيئة معالج الوسائط
            self.media_processor = MediaProcessor(self.config)
            
            # تهيئة واجهة المستخدم
            self.main_window = MainWindow(self.root, self.config, self.media_processor)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize application:\n{str(e)}")
            return False
    
    def setup_root_window(self):
        """إعداد النافذة الجذرية"""
        if self.root:
            # إعداد العنوان (إنجليزي فقط)
            self.root.title("Media Cut Pro")
            
            # تحديد حجم النافذة المثالي (أصغر ارتفاع)
            window_width = 650
            window_height = 370  # تقليل الارتفاع أكثر من 420 إلى 370
            
            # تحديد الحد الأدنى لحجم النافذة
            self.root.minsize(600, 350)  # تقليل الحد الأدنى أيضاً
            self.root.maxsize(800, 500)  # تقليل الحد الأقصى
            
            # توسيط النافذة على الشاشة
            self.center_window(window_width, window_height)
            
            # منع تغيير حجم النافذة بشكل مفرط
            self.root.resizable(True, False)
            
            # إعداد الأيقونة إذا كانت متوفرة
            self.setup_application_icon()
            
            # إعداد حدث إغلاق النافذة
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_application_icon(self):
        """إعداد أيقونة التطبيق لجميع النوافذ"""
        icon_path = os.path.join(project_root, "media cut pro.ico")
        if os.path.exists(icon_path):
            try:
                # تطبيق الأيقونة على النافذة الرئيسية
                self.root.iconbitmap(icon_path)
                
                # حفظ مسار الأيقونة لاستخدامه في النوافذ الأخرى
                self.root.icon_path = icon_path
                
                # تطبيق الأيقونة على جميع نوافذ Tkinter
                self.root.option_add('*Dialog.icon', icon_path)
                
            except Exception as e:
                print(f"خطأ في تحميل الأيقونة: {e}")
        else:
            print(f"ملف الأيقونة غير موجود: {icon_path}")
    
    def center_window(self, width, height):
        """توسيط النافذة على الشاشة"""
        if self.root:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_closing(self):
        """معالج حدث إغلاق التطبيق"""
        try:
            # إيقاف أي عمليات جارية
            if self.media_processor and hasattr(self.media_processor, 'stop_processing'):
                self.media_processor.stop_processing()
            
            # إغلاق النافذة
            if self.root:
                self.root.destroy()
                
        except Exception as e:
            print(f"خطأ أثناء إغلاق التطبيق: {e}")
        finally:
            sys.exit(0)
    
    def run(self):
        """تشغيل التطبيق"""
        if self.initialize():
            try:
                self.root.mainloop()
            except KeyboardInterrupt:
                self.on_closing()
            except Exception as e:
                messagebox.showerror("خطأ في التشغيل", f"حدث خطأ أثناء تشغيل التطبيق:\n{str(e)}")
                self.on_closing()
        else:
            sys.exit(1)

def main():
    """الدالة الرئيسية"""
    try:
        # إنشاء وتشغيل التطبيق
        app = MediaCutProApp()
        app.run()
        
    except Exception as e:
        print(f"خطأ فادح في التطبيق: {e}")
        if 'messagebox' in globals():
            messagebox.showerror("خطأ فادح", f"فشل في تشغيل التطبيق:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()