# -*- coding: utf-8 -*-
"""
نظام تنسيق الواجهة
يحتوي على تحسينات بصرية وتنسيق متقدم لواجهة Tkinter
"""

import tkinter as tk
from tkinter import ttk

class UIStyleManager:
    """مدير تنسيق الواجهة"""
    
    def __init__(self, root: tk.Tk, config):
        """تهيئة مدير التنسيق"""
        self.root = root
        self.config = config
        self.style = ttk.Style()
        
        # إعداد النمط
        self.setup_styles()
        self.configure_colors()
    
    def setup_styles(self):
        """إعداد أنماط TTK"""
        # تعيين النمط الأساسي
        available_themes = self.style.theme_names()
        if 'vista' in available_themes:
            self.style.theme_use('vista')
        elif 'winnative' in available_themes:
            self.style.theme_use('winnative')
        else:
            self.style.theme_use('default')
        
        # تخصيص أنماط الأزرار
        self.style.configure(
            "Accent.TButton",
            padding=(20, 10),
            font=('Segoe UI', 11, 'bold')
        )
        
        self.style.configure(
            "Success.TButton",
            padding=(15, 8)
        )
        
        self.style.configure(
            "Warning.TButton",
            padding=(15, 8)
        )
        
        # تخصيص شريط التقدم
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=25,
            troughcolor='#f0f0f0',
            background='#2c3e50',
            borderwidth=1,
            relief='flat'
        )
        
        # تخصيص LabelFrame
        self.style.configure(
            "Custom.TLabelframe",
            borderwidth=2,
            relief='groove'
        )
        
        self.style.configure(
            "Custom.TLabelframe.Label",
            font=('Segoe UI', 10, 'bold'),
            foreground='#2c3e50'
        )
    
    def configure_colors(self):
        """تكوين الألوان"""
        # ألوان الأزرار
        self.style.map("Accent.TButton",
            background=[
                ('active', '#3498db'),
                ('pressed', '#2980b9'),
                ('!disabled', '#34495e')
            ],
            foreground=[
                ('active', 'white'),
                ('pressed', 'white'),
                ('!disabled', 'white')
            ]
        )
        
        self.style.map("Success.TButton",
            background=[
                ('active', '#2ecc71'),
                ('pressed', '#27ae60'),
                ('!disabled', '#27ae60')
            ],
            foreground=[
                ('active', 'white'),
                ('pressed', 'white'),
                ('!disabled', 'white')
            ]
        )
        
        self.style.map("Warning.TButton",
            background=[
                ('active', '#f39c12'),
                ('pressed', '#e67e22'),
                ('!disabled', '#e74c3c')
            ],
            foreground=[
                ('active', 'white'),
                ('pressed', 'white'),
                ('!disabled', 'white')
            ]
        )
    
    def create_separator(self, parent, orient='horizontal'):
        """إنشاء خط فاصل"""
        separator = ttk.Separator(parent, orient=orient)
        return separator
    
    def create_info_label(self, parent, text, style='info'):
        """إنشاء تسمية معلوماتية"""
        colors = {
            'info': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }
        
        label = tk.Label(
            parent,
            text=text,
            font=self.config.fonts['small'],
            foreground=colors.get(style, '#3498db'),
            bg=self.root['bg']
        )
        return label
    
    def create_section_header(self, parent, text):
        """إنشاء عنوان قسم"""
        header = tk.Label(
            parent,
            text=text,
            font=('Segoe UI', 12, 'bold'),
            foreground='#2c3e50',
            bg=self.root['bg']
        )
        return header

class TooltipManager:
    """مدير التلميحات التفاعلية"""
    
    def __init__(self):
        self.tooltips = {}
    
    def add_tooltip(self, widget, text):
        """إضافة تلميح لعنصر واجهة"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#2c3e50')
            
            label = tk.Label(
                tooltip,
                text=text,
                background='#2c3e50',
                foreground='white',
                font=('Segoe UI', 9),
                padx=10,
                pady=5
            )
            label.pack()
            
            # موضع التلميح
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.geometry(f"+{x}+{y}")
            
            self.tooltips[widget] = tooltip
        
        def on_leave(event):
            tooltip = self.tooltips.get(widget)
            if tooltip:
                tooltip.destroy()
                del self.tooltips[widget]
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

class AnimationManager:
    """مدير الحركات البسيطة"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
    
    def fade_in(self, widget, duration=500):
        """تأثير ظهور تدريجي"""
        steps = 20
        step_time = duration // steps
        alpha_step = 1.0 / steps
        
        def animate_step(current_alpha, step):
            if step <= steps:
                try:
                    widget.configure(state='normal')
                    # تطبيق التأثير البصري
                    self.root.after(step_time, lambda: animate_step(current_alpha + alpha_step, step + 1))
                except:
                    pass
        
        animate_step(0, 1)
    
    def pulse_color(self, widget, color1, color2, duration=1000):
        """تأثير تغيير لون نابض"""
        def pulse():
            try:
                current_bg = widget.cget('background')
                new_color = color2 if current_bg == color1 else color1
                widget.configure(background=new_color)
                self.root.after(duration, pulse)
            except:
                pass
        
        pulse()

class ProgressIndicator:
    """مؤشر تقدم محسن"""
    
    def __init__(self, parent, style_manager):
        self.parent = parent
        self.style_manager = style_manager
        self.is_active = False
        
        # إطار المؤشر
        self.frame = ttk.Frame(parent)
        
        # إنشاء العناصر
        self.create_elements()
    
    def create_elements(self):
        """إنشاء عناصر المؤشر"""
        # عنوان الحالة
        self.status_label = tk.Label(
            self.frame,
            text="جاهز",
            font=('Segoe UI', 10, 'bold'),
            foreground='#2c3e50'
        )
        self.status_label.pack(pady=(0, 5))
        
        # شريط التقدم
        self.progress_bar = ttk.Progressbar(
            self.frame,
            mode='determinate',
            length=400,
            height=25,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=(0, 5))
        
        # تسمية النسبة المئوية
        self.percentage_label = tk.Label(
            self.frame,
            text="0%",
            font=('Segoe UI', 9),
            foreground='#7f8c8d'
        )
        self.percentage_label.pack()
        
        # تسمية الوقت المتبقي
        self.time_label = tk.Label(
            self.frame,
            text="",
            font=('Segoe UI', 8),
            foreground='#95a5a6'
        )
        self.time_label.pack()
    
    def update(self, percentage, status_text, time_remaining=None):
        """تحديث المؤشر"""
        self.progress_bar['value'] = percentage
        self.status_label.config(text=status_text)
        self.percentage_label.config(text=f"{percentage:.1f}%")
        
        if time_remaining:
            self.time_label.config(text=f"الوقت المتبقي: {time_remaining}")
        else:
            self.time_label.config(text="")
    
    def start_indeterminate(self, status_text="جاري المعالجة..."):
        """بدء وضع التقدم غير المحدد"""
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start(10)
        self.status_label.config(text=status_text)
        self.percentage_label.config(text="")
        self.is_active = True
    
    def stop_indeterminate(self):
        """إيقاف وضع التقدم غير المحدد"""
        if self.is_active:
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate')
            self.is_active = False
    
    def reset(self):
        """إعادة تعيين المؤشر"""
        self.stop_indeterminate()
        self.progress_bar['value'] = 0
        self.status_label.config(text="جاهز")
        self.percentage_label.config(text="0%")
        self.time_label.config(text="")
    
    def grid(self, **kwargs):
        """وضع المؤشر في الشبكة"""
        self.frame.grid(**kwargs)
    
    def pack(self, **kwargs):
        """وضع المؤشر بالتعبئة"""
        self.frame.pack(**kwargs)