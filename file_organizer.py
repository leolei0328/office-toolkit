#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文件分类整理工具 - 按类型/日期自动整理文件"""

import os
import shutil
from pathlib import Path
from datetime import datetime


EXT_MAP = {
    '图片': ['.jpg','.jpeg','.png','.gif','.bmp','.webp','.svg','.ico','.tiff'],
    '文档': ['.doc','.docx','.xls','.xlsx','.ppt','.pptx','.pdf','.txt','.md','.csv'],
    '视频': ['.mp4','.avi','.mkv','.mov','.wmv','.flv','.webm'],
    '音频': ['.mp3','.wav','.flac','.aac','.ogg','.wma'],
    '压缩包': ['.zip','.rar','.7z','.tar','.gz','.bz2'],
    '代码': ['.py','.js','.ts','.html','.css','.java','.cpp','.c','.h','.go','.rs','.sql','.sh','.bat'],
    '可执行程序': ['.exe','.msi','.app','.dmg','.deb','.rpm'],
}


def organize_by_type(directory, target_dir=None, dry_run=False):
    """按文件类型分类整理"""
    dir_path = Path(directory)
    if not dir_path.exists():
        return False, f"目录不存在: {directory}"
    
    target = Path(target_dir) if target_dir else dir_path
    files = [f for f in dir_path.iterdir() if f.is_file()]
    
    moved = 0
    not_moved = 0
    
    for f in files:
        ext = f.suffix.lower()
        category = '其他'
        for cat, exts in EXT_MAP.items():
            if ext in exts:
                category = cat
                break
        
        dest = target / category
        if dry_run:
            print(f"[模拟] {f.name} -> {dest.name}/")
            not_moved += 1
            continue
        
        dest.mkdir(exist_ok=True)
        dest_file = dest / f.name
        if dest_file.exists():
            dest_file = dest / f"{f.stem}_{datetime.now().strftime('%H%M%S')}{f.suffix}"
        shutil.move(str(f), str(dest_file))
        moved += 1
    
    msg = f"成功整理 {moved} 个文件" if not dry_run else f"将整理 {not_moved} 个文件"
    return True, msg


def organize_by_date(directory, target_dir=None, date_source='mtime', dry_run=False):
    """按日期分类整理（年/月/日）"""
    dir_path = Path(directory)
    if not dir_path.exists():
        return False, f"目录不存在: {directory}"
    
    target = Path(target_dir) if target_dir else dir_path
    files = [f for f in dir_path.iterdir() if f.is_file()]
    
    moved = 0
    for f in files:
        try:
            if date_source == 'mtime':
                ts = os.path.getmtime(f)
            elif date_source == 'ctime':
                ts = os.path.getctime(f)
            else:
                ts = os.path.getmtime(f)
            dt = datetime.fromtimestamp(ts)
            sub = f"{dt.year}/{dt.month:02d}"
        except:
            sub = "未知日期"
        
        dest = target / sub
        if dry_run:
            print(f"[模拟] {f.name} -> {dest}/")
            not_moved = 0 if not_moved else 0  # no-op
            continue
        
        dest.mkdir(parents=True, exist_ok=True)
        dest_file = dest / f.name
        if dest_file.exists():    
            dest_file = dest / f"{f.stem}_{datetime.now().strftime('%H%M%S')}{f.suffix}"
        shutil.move(str(f), str(dest_file))
        moved += 1
    
    return True, f"成功整理 {moved} 个文件" if not dry_run else f"将整理 {moved} 个文件"


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    
    root = tk.Tk()
    root.title("文件分类整理工具")
    root.geometry("550x400")
    root.resizable(False, False)
    
    tk.Label(root, text="文件分类整理工具", font=("", 16, "bold")).pack(pady=10)
    
    tk.Label(root, text="选择要整理的目录:").pack(anchor=tk.W, padx=20, pady=(5,0))
    f1 = tk.Frame(root); f1.pack(fill=tk.X, padx=20, pady=5)
    dir_var = tk.StringVar()
    tk.Entry(f1, textvariable=dir_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(f1, text="浏览...", command=lambda: dir_var.set(filedialog.askdirectory())).pack(side=tk.RIGHT, padx=(5,0))
    
    mode_var = tk.StringVar(value="type")
    fm = tk.Frame(root); fm.pack(pady=10)
    tk.Radiobutton(fm, text="按文件类型整理", variable=mode_var, value="type").pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(fm, text="按日期整理", variable=mode_var, value="date").pack(side=tk.LEFT, padx=10)
    
    dry_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="先预览（模拟运行）", variable=dry_var).pack(pady=5)
    
    log_text = tk.Text(root, height=8, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    
    def run():
        d = dir_var.get().strip()
        if not d: messagebox.showerror("错误", "请选择目录"); return
        
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, "正在整理...\n")
        log_text.config(state=tk.DISABLED)
        root.update()
        
        if mode_var.get() == "type":
            s, m = organize_by_type(d, dry_run=dry_var.get())
        else:
            s, m = organize_by_date(d, dry_run=dry_var.get())
        
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, m+"\n")
        log_text.config(state=tk.DISABLED)
        if s and not dry_var.get(): messagebox.showinfo("完成", m)
    
    def run_real():
        old = dry_var.get()
        dry_var.set(False)
        run()
        dry_var.set(old)
    
    btnf = tk.Frame(root); btnf.pack(pady=10)
    tk.Button(btnf, text="预览", command=run).pack(side=tk.LEFT, padx=5)
    tk.Button(btnf, text="执行整理", command=run_real, bg="#4CAF50", fg="white", font=("", 12, "bold")).pack(side=tk.LEFT, padx=5)
    
    root.mainloop()


if __name__ == "__main__":
    main()
