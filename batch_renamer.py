#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量重命名工具"""

import os
import re
import sys
from pathlib import Path


def batch_rename(directory, rule, **kwargs):
    """
    批量重命名文件
    
    Rules:
        'prefix': 添加前缀, kwargs: text
        'suffix': 添加后缀, kwargs: text
        'replace': 替换文字, kwargs: old, new
        'numbered': 编号重命名, kwargs: prefix, start, digits
        'regex': 正则替换, kwargs: pattern, replacement
        'ext': 修改扩展名, kwargs: new_ext
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return False, f"目录不存在: {directory}"
    
    files = [f for f in dir_path.iterdir() if f.is_file()]
    if not files:
        return False, "目录下没有文件"
    
    renamed = 0
    errors = []
    
    for f in files:
        stem = f.stem
        ext = f.suffix
        new_name = stem
        
        try:
            if rule == 'prefix':
                new_name = kwargs['text'] + stem
            elif rule == 'suffix':
                new_name = stem + kwargs['text']
            elif rule == 'replace':
                new_name = stem.replace(kwargs['old'], kwargs['new'])
            elif rule == 'numbered':
                n = str(renamed + kwargs.get('start', 1)).zfill(kwargs.get('digits', 3))
                new_name = kwargs.get('prefix', '') + n
            elif rule == 'regex':
                new_name = re.sub(kwargs['pattern'], kwargs['replacement'], stem)
            elif rule == 'ext':
                new_ext = kwargs['new_ext'] if kwargs['new_ext'].startswith('.') else '.' + kwargs['new_ext']
                new_path = f.parent / (stem + new_ext)
                os.rename(f, new_path)
                renamed += 1
                continue
            
            new_path = f.parent / (new_name + ext)
            if new_path != f:
                if new_path.exists():
                    errors.append(f"跳过 {f.name}: 目标文件已存在")
                    continue
                os.rename(f, new_path)
                renamed += 1
        except Exception as e:
            errors.append(f"{f.name}: {str(e)}")
    
    msg = f"成功重命名 {renamed} 个文件"
    if errors:
        msg += "\n" + "\n".join(errors[:5])
    return True, msg


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    
    root = tk.Tk()
    root.title("批量重命名工具")
    root.geometry("600x500")
    root.resizable(False, False)
    
    tk.Label(root, text="批量重命名工具", font=("", 16, "bold")).pack(pady=10)
    
    tk.Label(root, text="选择目录:").pack(anchor=tk.W, padx=20)
    f1 = tk.Frame(root); f1.pack(fill=tk.X, padx=20, pady=5)
    dir_var = tk.StringVar()
    tk.Entry(f1, textvariable=dir_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(f1, text="浏览...", command=lambda: dir_var.set(filedialog.askdirectory())).pack(side=tk.RIGHT, padx=(5,0))
    
    tk.Label(root, text="重命名规则:").pack(anchor=tk.W, padx=20, pady=(10,0))
    
    rule_var = tk.StringVar(value="numbered")
    frame = tk.Frame(root)
    frame.pack(fill=tk.X, padx=20, pady=5)
    
    rules_frame = tk.Frame(frame)
    rules_frame.pack(fill=tk.X)
    for i, (val, text) in enumerate([("numbered","编号重命名"), ("prefix","添加前缀"), ("suffix","添加后缀"), ("replace","替换文字"), ("regex","正则替换"), ("ext","修改扩展名")]):
        tk.Radiobutton(rules_frame, text=text, variable=rule_var, value=val).grid(row=i//3, column=i%3, sticky=tk.W, padx=5)
    
    # Options
    opt_frame = tk.LabelFrame(root, text="规则参数", padx=10, pady=10)
    opt_frame.pack(fill=tk.X, padx=20, pady=10)
    
    opt_widgets = {}
    opt_rows = [
        ("numbered", [("文件名前缀","prefix_var","file_"), ("起始编号","start_var","1"), ("位数","digits_var","3")]),
        ("prefix", [("添加的文字","pre_text_var","")]),
        ("suffix", [("添加的文字","suf_text_var","")]),
        ("replace", [("查找文字","old_var",""), ("替换为","new_var","")]),
        ("regex", [("正则表达式","pattern_var",""), ("替换为","replacement_var","")]),
        ("ext", [("新扩展名","ext_var",".txt")]),
    ]
    
    vars_map = {}
    for rule_type, fields in opt_rows:
        for label, vname, default in fields:
            vars_map[vname] = tk.StringVar(value=default)
            row = tk.Frame(opt_frame)
            tk.Label(row, text=label, width=10, anchor=tk.W).pack(side=tk.LEFT)
            tk.Entry(row, textvariable=vars_map[vname]).pack(side=tk.LEFT, fill=tk.X, expand=True)
            row.pack(fill=tk.X, pady=2)
            row.pack_forget()
            opt_widgets.setdefault(rule_type, []).append(row)
    
    def show_opts(*args):
        for k, rows in opt_widgets.items():
            for r in rows: r.pack_forget()
        for r in opt_widgets.get(rule_var.get(), []):
            r.pack(fill=tk.X, pady=2)
    rule_var.trace('w', show_opts)
    show_opts()
    
    log_text = tk.Text(root, height=6, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    
    def run():
        d = dir_var.get().strip()
        if not d: messagebox.showerror("错误", "请选择目录"); return
        
        kwargs = {
            'prefix': vars_map['prefix_var'].get(),
            'start': int(vars_map['start_var'].get()) if vars_map['start_var'].get().isdigit() else 1,
            'digits': int(vars_map['digits_var'].get()) if vars_map['digits_var'].get().isdigit() else 3,
            'text': vars_map['pre_text_var'].get() or vars_map['suf_text_var'].get(),
            'old': vars_map['old_var'].get(),
            'new': vars_map['new_var'].get(),
            'pattern': vars_map['pattern_var'].get(),
            'replacement': vars_map['replacement_var'].get(),
            'new_ext': vars_map['ext_var'].get(),
        }
        
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f"正在重命名...\n")
        log_text.config(state=tk.DISABLED)
        root.update()
        
        s, m = batch_rename(d, rule_var.get(), **kwargs)
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, m+"\n")
        log_text.config(state=tk.DISABLED)
        if s: messagebox.showinfo("完成", m)
    
    tk.Button(root, text="开始重命名", command=run, bg="#4CAF50", fg="white", font=("", 12, "bold")).pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()
