#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""办公自动化工具箱 - 图形界面启动器"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from pathlib import Path


TOOLS = [
    {
        'name': 'Excel批量合并',
        'icon': '📊',
        'desc': '将多个Excel文件合并为一个，支持按行追加合并',
        'module': 'tools.excel_merger',
        'color': '#2196F3',
    },
    {
        'name': 'Excel拆分',
        'icon': '✂️',
        'desc': '按列值或行数将Excel拆分为多个文件',
        'module': 'tools.excel_splitter',
        'color': '#9C27B0',
    },
    {
        'name': '批量重命名',
        'icon': '🏷️',
        'desc': '按规则批量重命名文件，支持编号/前缀/替换/正则',
        'module': 'tools.batch_renamer',
        'color': '#FF9800',
    },
    {
        'name': '图片批量处理',
        'icon': '🖼️',
        'desc': '批量缩放、压缩、格式转换、添加水印',
        'module': 'tools.image_batch',
        'color': '#4CAF50',
    },
    {
        'name': 'PDF报表生成',
        'icon': '📄',
        'desc': '从数据自动生成专业PDF报表和报价单',
        'module': 'tools.pdf_report',
        'color': '#F44336',
    },
    {
        'name': '文件分类整理',
        'icon': '📁',
        'desc': '按文件类型或日期自动整理文件到分类目录',
        'module': 'tools.file_organizer',
        'color': '#607D8B',
    },
]


class ToolLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("办公自动化工具箱 v1.0")
        self.root.geometry("700x520")
        self.root.resizable(False, False)
        
        # Header
        header = tk.Frame(self.root, bg='#1a237e', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🔧 办公自动化工具箱", font=("", 22, "bold"),
                 fg='white', bg='#1a237e').pack(pady=(10,0))
        tk.Label(header, text="提升工作效率 · 一键搞定重复劳动", font=("", 11),
                 fg='#90caf9', bg='#1a237e').pack()
        
        # Tools grid
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="选择工具:", font=("", 14, "bold")).pack(anchor=tk.W)
        
        tools_frame = tk.Frame(main_frame)
        tools_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for i, tool in enumerate(TOOLS):
            self._create_tool_card(tools_frame, tool, i // 2, i % 2)
        
        # Footer with donation button
        footer = tk.Frame(self.root, bg='#f5f5f5', height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        # Donation button
        donate_btn = tk.Label(footer, text="☕ 请作者喝咖啡", font=("", 9, "bold"),
                              fg='#E65100', bg='#f5f5f5', cursor='hand2')
        donate_btn.pack(side=tk.RIGHT, padx=10)
        donate_btn.bind('<Button-1>', lambda e: self._show_donate())
        
        tk.Label(footer, text="运行环境: Python 3", 
                 font=("", 9), fg='#888', bg='#f5f5f5').pack(side=tk.LEFT, padx=10)
    
    def _show_donate(self):
        from PIL import Image, ImageTk
        donate_win = tk.Toplevel(self.root)
        donate_win.title("赞助支持")
        donate_win.geometry("320x420")
        donate_win.resizable(False, False)
        donate_win.configure(bg='white')
        
        tk.Label(donate_win, text="☕ 如果这个工具帮到了你", font=("", 12),
                 bg='white', fg='#333').pack(pady=(15,5))
        tk.Label(donate_win, text="欢迎请作者喝杯咖啡", font=("", 10),
                 bg='white', fg='#888').pack()
        
        img_path = Path(__file__).parent / 'donate_qr.jpg'
        if img_path.exists():
            img = Image.open(img_path)
            img.thumbnail((280, 280))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(donate_win, image=photo, bg='white')
            img_label.image = photo
            img_label.pack(pady=10)
        else:
            tk.Label(donate_win, text="(收款码加载中)", font=("", 9),
                     fg='#999', bg='white').pack(pady=30)
        
        tk.Label(donate_win, text="微信扫码 · 随缘打赏", font=("", 9),
                 fg='#666', bg='white').pack()
        tk.Button(donate_win, text="关闭", command=donate_win.destroy,
                  bg='#eee', relief=tk.FLAT).pack(pady=10)

    def _create_tool_card(self, parent, tool, row, col):
        frame = tk.Frame(parent, bd=1, relief=tk.RAISED, padx=10, pady=10, cursor='hand2')
        frame.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        icon_color = tk.Frame(frame, bg=tool['color'], width=40, height=40)
        icon_color.pack(side=tk.LEFT, padx=(0,10))
        icon_color.pack_propagate(False)
        tk.Label(icon_color, text=tool['icon'], font=("", 20), bg=tool['color']).pack(expand=True)
        
        text_frame = tk.Frame(frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(text_frame, text=tool['name'], font=("", 13, "bold"), fg=tool['color']).pack(anchor=tk.W)
        tk.Label(text_frame, text=tool['desc'], font=("", 9), fg='#666', wraplength=200, justify=tk.LEFT).pack(anchor=tk.W)
        
        def launch(event=None):
            self._launch_tool(tool)
        
        for widget in [frame, icon_color, text_frame]:
            widget.bind('<Button-1>', launch)
            for child in widget.winfo_children():
                child.bind('<Button-1>', launch)
        
        frame.bind('<Enter>', lambda e, f=frame: f.configure(bg='#e3f2fd'))
        frame.bind('<Leave>', lambda e, f=frame: f.configure(bg='SystemButtonFace'))
        for w in frame.winfo_children():
            w.bind('<Enter>', lambda e, f=frame: f.configure(bg='#e3f2fd'))
            w.bind('<Leave>', lambda e, f=frame: f.configure(bg='SystemButtonFace'))
    
    def _launch_tool(self, tool):
        try:
            root_dir = Path(__file__).parent
            os.chdir(root_dir)
            script_path = root_dir / 'tools' / f'{tool["module"].split(".")[1]}.py'
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            messagebox.showerror("启动失败", f"无法启动 {tool['name']}: {str(e)}")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ToolLauncher()
    app.run()
