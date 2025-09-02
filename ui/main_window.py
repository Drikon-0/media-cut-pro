# -*- coding: utf-8 -*-
"""
Main application window - simplified and optimized version
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import time

class MainWindow:
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self, root, config, media_processor):
        """تهيئة النافذة الرئيسية"""
        self.root = root
        self.config = config
        self.media_processor = media_processor
        
        # متغيرات الواجهة
        self.selected_file = tk.StringVar()
        self.split_duration = tk.DoubleVar(value=10.0)
        self.output_format = tk.StringVar()
        self.output_directory = tk.StringVar()
        
        # حالة المعالجة
        self.is_processing = False
        self.last_output_path = ""
        
        # متغيرات الأنيميشن
        self.spinner_pattern = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.spinner_index = 0
        self.animation_thread = None
        self.animation_running = False
        
        # أنيميشن شريط الحالة المستمر
        self.status_spinner_thread = None
        self.status_animation_running = False
        
        # متغيرات التقدم المحسنة
        self.current_progress = 0.0
        self.current_message = "Ready"
        self.smooth_update_thread = None
        
        # إعداد الواجهة
        self.setup_ui()
        self.setup_callbacks()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم المبسطة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root, padding="8")  # تقليل padding
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان مع حقوق الطبع والنشر
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 10))
        
        # العنوان الرئيسي
        title_label = tk.Label(
            title_frame, 
            text="🎬 Media Cut Pro",
            font=('Segoe UI', 14, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack()
        
        # حقوق الطبع والنشر
        copyright_label = tk.Label(
            title_frame,
            text="By Drikon",
            font=('Segoe UI', 8),
            fg='#7f8c8d'  # لون رمادي
        )
        copyright_label.pack()
        
        # أقسام الواجهة
        self.create_file_section(main_frame)
        self.create_settings_section(main_frame)
        self.create_control_section(main_frame)
        self.create_progress_section(main_frame)
        self.setup_status_bar(main_frame)  # إضافة شريط الحالة
    
    def create_file_section(self, parent):
        """إنشاء قسم اختيار الملف"""
        file_frame = ttk.LabelFrame(parent, text="📁 Choose File", padding="8")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # صف واحد
        row = ttk.Frame(file_frame)
        row.pack(fill=tk.X)
        
        # زر تصفح
        browse_btn = ttk.Button(row, text="تصفح", command=self.browse_file, width=8)
        browse_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # مربع النص
        self.file_entry = ttk.Entry(
            row, 
            textvariable=self.selected_file, 
            state="readonly",
            font=('Segoe UI', 9)
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # زر مسح
        clear_btn = ttk.Button(row, text="✖", command=self.clear_file, width=3)
        clear_btn.pack(side=tk.LEFT)
    
    def create_settings_section(self, parent):
        """إنشاء قسم الإعدادات المبسط"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Split Settings", padding="8")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول
        row1 = ttk.Frame(settings_frame)
        row1.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(row1, text="مدة الجزء (دقائق):", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        duration_spin = ttk.Spinbox(
            row1, 
            from_=1, 
            to=120, 
            textvariable=self.split_duration,
            width=6,
            font=('Segoe UI', 9)
        )
        duration_spin.pack(side=tk.LEFT, padx=(8, 15))
        
        tk.Label(row1, text="صيغة الإخراج:", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        self.format_combo = ttk.Combobox(
            row1, 
            textvariable=self.output_format,
            state="readonly",
            width=16,
            font=('Segoe UI', 9)
        )
        self.format_combo.pack(side=tk.LEFT, padx=(8, 0))
        
        # الصف الثاني
        row2 = ttk.Frame(settings_frame)
        row2.pack(fill=tk.X)
        
        tk.Label(row2, text="Output Directory (optional):", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        self.output_entry = ttk.Entry(
            row2, 
            textvariable=self.output_directory,
            font=('Segoe UI', 9)
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))
        
        output_btn = ttk.Button(row2, text="...", command=self.browse_output, width=3)
        output_btn.pack(side=tk.LEFT)
    
    def create_control_section(self, parent):
        """إنشاء قسم التحكم"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # مركز الأزرار
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()
        
        # زر البدء
        self.start_btn = ttk.Button(
            button_frame,
            text="▶️ Start Splitting",
            command=self.start_processing
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # زر الإيقاف
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_processing,
            state="disabled"
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # زر فتح المجلد
        self.open_btn = ttk.Button(
            button_frame,
            text="📁 Open Folder",
            command=self.open_output_folder,
            state="disabled"
        )
        self.open_btn.pack(side=tk.LEFT)
    
    def create_progress_section(self, parent):
        """إنشاء قسم التقدم"""
        progress_frame = ttk.LabelFrame(parent, text="📊 التقدم", padding="8")
        progress_frame.pack(fill=tk.X)
        
        # شريط التقدم
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # نص معلومات التقدم مع الأنيميشن
        progress_info_frame = tk.Frame(progress_frame)
        progress_info_frame.pack(fill=tk.X)
        
        # الأنيميشن على اليسار
        self.spinner_var = tk.StringVar(value="")  # فارغ في البداية
        spinner_label = tk.Label(
            progress_info_frame,
            textvariable=self.spinner_var,
            font=('Segoe UI', 10),
            fg='#3498db'
        )
        spinner_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # معلومات التقدم بجانب الأنيميشن
        self.progress_info_var = tk.StringVar(value="")
        progress_info_label = tk.Label(
            progress_info_frame,
            textvariable=self.progress_info_var,
            font=('Segoe UI', 8),
            fg='#34495e'
        )
        progress_info_label.pack(side=tk.LEFT)
        
        # السبينر سيبدأ عند بدء التقطيع
    
    def show_message_with_icon(self, msg_type, title, message):
        """عرض رسالة مع تطبيق أيقونة التطبيق"""
        # إنشاء نافذة مؤقتة لتطبيق الأيقونة
        dialog = tk.Toplevel(self.root)
        dialog.withdraw()  # إخفاؤها مؤقتاً
        
        # تطبيق الأيقونة إذا كانت متوفرة
        if hasattr(self.root, 'icon_path'):
            try:
                dialog.iconbitmap(self.root.icon_path)
            except:
                pass
        
        dialog.destroy()
        
        # عرض الرسالة العادية
        if msg_type == "info":
            return messagebox.showinfo(title, message)
        elif msg_type == "error":
            return messagebox.showerror(title, message)
        elif msg_type == "warning":
            return messagebox.showwarning(title, message)
        elif msg_type == "question":
            return messagebox.askyesno(title, message)
    
    def setup_status_bar(self, parent):
        """إعداد شريط الحالة في أسفل النافذة"""
        # فاصل بصري
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill=tk.X, pady=(5, 5))
        
        # إطار شريط الحالة مع خلفية مميزة
        status_frame = tk.Frame(parent, bg='#ecf0f1', relief='sunken', bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 5), padx=5)
        
        # نص الحالة مع الأنيميشن
        self.status_var = tk.StringVar(value="⠋ Ready")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 9, 'bold'),  
            fg='#2c3e50',
            bg='#ecf0f1',  # نفس خلفية الإطار
            anchor='w',
            padx=8,
            pady=3
        )
        status_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # السبينر سيبدأ عند بدء التقطيع بدلاً من إقلاع البرنامج
    
    def start_status_animation(self):
        """بدء أنيميشن الـ spinner في قسم التقدم"""
        if not self.status_animation_running:
            self.status_animation_running = True
            # تحديث فوري أولاً
            self.spinner_var.set("⠋")
            # بدء الخيط
            self.status_spinner_thread = threading.Thread(target=self._animate_status_spinner, daemon=True)
            self.status_spinner_thread.start()
    
    def stop_status_animation(self):
        """إيقاف أنيميشن شريط الحالة"""
        self.status_animation_running = False
        if self.status_spinner_thread and self.status_spinner_thread.is_alive():
            self.status_spinner_thread.join(timeout=0.1)
        self.status_spinner_thread = None
    
    def _animate_status_spinner(self):
        """دوران الأنيميشن في قسم التقدم بجانب النسبة المئوية"""
        while self.status_animation_running:
            try:
                # الحصول على الرمز الحالي للأنيميشن
                spinner = self.spinner_pattern[self.spinner_index % len(self.spinner_pattern)]
                
                # تحديث الأنيميشن بأمان
                self.root.after(0, lambda text=spinner: self.spinner_var.set(text))
                
                # تحديث مؤشر الأنيميشن
                self.spinner_index = (self.spinner_index + 1) % len(self.spinner_pattern)
                
                time.sleep(0.1)  # سرعة دوران أسرع
                
            except Exception:
                break
    
    def setup_callbacks(self):
        """إعداد الاستدعاءات"""
        self.selected_file.trace_add('write', self.on_file_changed)
        self.media_processor.set_progress_callback(self.update_progress)
        self.media_processor.set_completion_callback(self.on_processing_completed)
    
    def browse_file(self):
        """تصفح الملفات"""
        file_types = [
            ("ملفات الوسائط", "*.mp4 *.mkv *.mov *.avi *.mp3 *.wav *.flac *.aac"),
            ("ملفات الفيديو", "*.mp4 *.mkv *.mov *.avi"),
            ("ملفات الصوت", "*.mp3 *.wav *.flac *.aac"),
            ("جميع الملفات", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="اختر ملف وسائط",
            filetypes=file_types
        )
        
        if filename:
            self.selected_file.set(filename)
    
    def clear_file(self):
        """مسح الملف"""
        self.selected_file.set("")
        self.output_format.set("")
        self.output_directory.set("")
    
    def browse_output(self):
        """تصفح مجلد الإخراج"""
        directory = filedialog.askdirectory(title="اختر مجلد الإخراج")
        if directory:
            self.output_directory.set(directory)
    
    def on_file_changed(self, *args):
        """معالج تغيير الملف"""
        file_path = self.selected_file.get()
        
        if file_path and os.path.exists(file_path):
            try:
                formats = self.config.get_output_formats_for_file(file_path)
                if formats:
                    format_list = [f"{key} - {value.get('description', key)}" for key, value in formats.items()]
                    self.format_combo['values'] = format_list
                    if format_list:
                        self.output_format.set(format_list[0])
                else:
                    self.format_combo['values'] = ()
                    self.output_format.set("")
            except Exception:
                self.format_combo['values'] = ()
                self.output_format.set("")
        else:
            self.format_combo['values'] = ()
            self.output_format.set("")
    
    def start_processing(self):
        """بدء المعالجة"""
        if not self.validate_inputs():
            return
        
        self.is_processing = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.open_btn.config(state="disabled")
        
        # تحديث نص الحالة فوراً
        self.status_var.set("🚀 بدء المعالجة...")
        
        # بدء أنيميشن السبينر
        self.start_status_animation()
        
        # بدء الأنيميشن
        self.start_animation()
        
        input_file = self.selected_file.get()
        duration = self.split_duration.get()
        format_text = self.output_format.get()
        output_format = format_text.split(' - ')[0] if ' - ' in format_text else format_text
        output_dir = self.output_directory.get() if self.output_directory.get() else None
        
        success = self.media_processor.process_media_file_async(
            input_file, duration, output_format, output_dir
        )
        
        if not success:
            self.on_processing_completed(False, "فشل في بدء المعالجة", "")
    
    def stop_processing(self):
        """إيقاف المعالجة"""
        if self.is_processing:
            self.media_processor.stop_processing()
            self.stop_animation()  # إيقاف الأنيميشن
    
    def validate_inputs(self):
        """التحقق من المدخلات"""
        if not self.selected_file.get():
            self.show_message_with_icon("error", "خطأ", "يجب اختيار ملف أولاً")
            return False
        
        if not os.path.exists(self.selected_file.get()):
            self.show_message_with_icon("error", "خطأ", "الملف غير موجود")
            return False
        
        if not self.output_format.get():
            self.show_message_with_icon("error", "خطأ", "يجب اختيار صيغة الإخراج")
            return False
        
        if self.split_duration.get() < 1:
            self.show_message_with_icon("error", "خطأ", "الحد الأدنى للمدة دقيقة واحدة")
            return False
        
        return True
    
    def update_progress(self, percentage, message):
        """تحديث التقدم مع عرض المعلومات في المكان المناسب"""
        # تحديث التقدم والرسالة بشكل آمن
        self.current_progress = float(percentage)
        self.current_message = str(message)
        
        # تحديث شريط التقدم
        self.root.after(0, lambda: self.progress_var.set(self.current_progress))
        
        # عرض معلومات التقدم في المكان المخصص
        if self.current_progress > 0:
            progress_text = f"{self.current_message} ({self.current_progress:.1f}%)"
            self.root.after(0, lambda: self.progress_info_var.set(progress_text))
        else:
            self.root.after(0, lambda: self.progress_info_var.set(""))
        
        # إجباري تحديث الواجهة
        self.root.update_idletasks()
    
    def start_animation(self):
        """بدء الأنيميشن المستمر"""
        if not self.animation_running:
            self.animation_running = True
            self.animation_thread = threading.Thread(target=self._animate_spinner, daemon=True)
            self.animation_thread.start()
    
    def start_smooth_updates(self):
        """بدء التحديثات السلسة للنص"""
        if not self.smooth_update_thread:
            self.smooth_update_thread = threading.Thread(target=self._smooth_text_updates, daemon=True)
            self.smooth_update_thread.start()
    
    def stop_animation(self):
        """إيقاف الأنيميشن"""
        self.animation_running = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=0.1)
        
        if self.smooth_update_thread and self.smooth_update_thread.is_alive():
            self.smooth_update_thread.join(timeout=0.1)
        
        self.smooth_update_thread = None
    
    def _animate_spinner(self):
        """تحديث الأنيميشن في خيط منفصل - يستمر في الدوران"""
        while self.animation_running:
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_pattern)
            time.sleep(0.2)  # سرعة دوران أبطأ قليلاً لوضوح أكثر
    
    def _smooth_text_updates(self):
        """تحديث النص بسلاسة مع الأنيميشن"""
        while self.animation_running and self.is_processing:
            try:
                # الحصول على الرمز الحالي للأنيميشن
                spinner = self.spinner_pattern[self.spinner_index % len(self.spinner_pattern)]
                
                # تنسيق الرسالة مع الأنيميشن والنسبة
                if self.current_progress < 100:
                    animated_text = f"{spinner} {self.current_message} ({self.current_progress:.1f}%)"
                else:
                    animated_text = f"✅ {self.current_message} (100.0%)"
                
                # تحديث النص بأمان
                self.root.after(0, lambda text=animated_text: self.status_var.set(text))
                
                time.sleep(0.2)  # تحديث النص مع الأنيميشن - أبطأ لوضوح أكثر
                
            except Exception:
                break
    
    def on_processing_completed(self, success, message, output_path):
        """إنجاز المعالجة"""
        self.is_processing = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
        # إيقاف الأنيميشن
        self.stop_animation()
        # إيقاف أنيميشن السبينر
        self.stop_status_animation()
        
        # إعادة تعيين متغيرات التقدم
        self.current_progress = 0.0
        self.progress_info_var.set("")  # إخفاء معلومات التقدم
        self.spinner_var.set("●")  # رمز ثابت عند الانتهاء
        
        if success:
            self.show_message_with_icon("info", "تم بنجاح! ✅", message)
            self.open_btn.config(state="normal")
            self.last_output_path = output_path
            self.current_message = "تم بنجاح"
        else:
            self.show_message_with_icon("error", "فشل ❌", message)
            self.progress_var.set(0)
            self.current_message = "جاهز"
    
    def open_output_folder(self):
        """فتح مجلد الإخراج"""
        if self.last_output_path and os.path.exists(self.last_output_path):
            os.startfile(self.last_output_path)
        else:
            self.show_message_with_icon("error", "خطأ", "المجلد غير موجود")