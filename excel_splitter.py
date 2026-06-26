#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Excel拆分工具 - 按条件将一个Excel拆分为多个文件"""

import pandas as pd
import os
import sys
from pathlib import Path


def split_excel_by_column(input_file, column, output_dir, file_prefix=""):
    """
    按指定列的值将Excel拆分为多个文件
    
    Args:
        input_file: 输入的Excel文件路径
        column: 拆分的列名
        output_dir: 输出目录
        file_prefix: 输出文件前缀
    """
    if not os.path.exists(input_file):
        return False, f"文件不存在: {input_file}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df = pd.read_excel(input_file)
        if column not in df.columns:
            return False, f"找不到列: {column}，可用列: {', '.join(df.columns.tolist())}"
        
        groups = df.groupby(column)
        count = 0
        for name, group in groups:
            safe_name = str(name).replace('/', '_').replace('\\', '_').replace(':', '_')
            output_file = os.path.join(output_dir, f"{file_prefix}{safe_name}.xlsx")
            group.to_excel(output_file, index=False)
            count += 1
        
        return True, f"成功拆分为 {count} 个文件，保存至 {output_dir}"
    except Exception as e:
        return False, f"拆分失败: {str(e)}"


def split_excel_by_rows(input_file, rows_per_file, output_dir, file_prefix=""):
    """按行数拆分Excel"""
    if not os.path.exists(input_file):
        return False, f"文件不存在: {input_file}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df = pd.read_excel(input_file)
        total = len(df)
        count = 0
        for i in range(0, total, rows_per_file):
            chunk = df.iloc[i:i+rows_per_file]
            part_num = i // rows_per_file + 1
            output_file = os.path.join(output_dir, f"{file_prefix}第{part_num}部分.xlsx")
            chunk.to_excel(output_file, index=False)
            count += 1
        
        return True, f"成功拆分为 {count} 个文件，保存至 {output_dir}"
    except Exception as e:
        return False, f"拆分失败: {str(e)}"


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    
    root = tk.Tk()
    root.title("Excel拆分工具")
    root.geometry("620x550")
    root.resizable(False, False)
    
    tk.Label(root, text="Excel拆分工具", font=("", 16, "bold")).pack(pady=10)
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Tab 1: By column
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text="按列拆分")
    
    tk.Label(tab1, text="输入Excel文件:").pack(anchor=tk.W, pady=(10,0))
    f1 = tk.Frame(tab1); f1.pack(fill=tk.X, pady=5)
    f1_var = tk.StringVar()
    tk.Entry(f1, textvariable=f1_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(f1, text="浏览...", command=lambda: f1_var.set(filedialog.askopenfilename(filetypes=[("Excel文件","*.xlsx *.xls")]))).pack(side=tk.RIGHT, padx=(5,0))
    
    tk.Label(tab1, text="按哪一列拆分:").pack(anchor=tk.W, pady=(5,0))
    col1_var = tk.StringVar()
    tk.Entry(tab1, textvariable=col1_var).pack(fill=tk.X, pady=5)
    
    tk.Label(tab1, text="输出目录:").pack(anchor=tk.W, pady=(5,0))
    d1 = tk.Frame(tab1); d1.pack(fill=tk.X, pady=5)
    od1_var = tk.StringVar()
    tk.Entry(d1, textvariable=od1_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(d1, text="浏览...", command=lambda: od1_var.set(filedialog.askdirectory())).pack(side=tk.RIGHT, padx=(5,0))
    
    log1 = tk.Text(tab1, height=6, state=tk.DISABLED)
    log1.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def run1():
        s, m = split_excel_by_column(f1_var.get(), col1_var.get(), od1_var.get())
        log1.config(state=tk.NORMAL); log1.insert(tk.END, m+"\n"); log1.config(state=tk.DISABLED)
        if s: messagebox.showinfo("完成", m)
    tk.Button(tab1, text="开始拆分", command=run1, bg="#4CAF50", fg="white").pack(pady=5)
    
    # Tab 2: By rows
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="按行数拆分")
    
    tk.Label(tab2, text="输入Excel文件:").pack(anchor=tk.W, pady=(10,0))
    f2 = tk.Frame(tab2); f2.pack(fill=tk.X, pady=5)
    f2_var = tk.StringVar()
    tk.Entry(f2, textvariable=f2_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(f2, text="浏览...", command=lambda: f2_var.set(filedialog.askopenfilename(filetypes=[("Excel文件","*.xlsx *.xls")]))).pack(side=tk.RIGHT, padx=(5,0))
    
    tk.Label(tab2, text="每个文件的行数:").pack(anchor=tk.W, pady=(5,0))
    row_var = tk.StringVar(value="1000")
    tk.Entry(tab2, textvariable=row_var).pack(fill=tk.X, pady=5)
    
    tk.Label(tab2, text="输出目录:").pack(anchor=tk.W, pady=(5,0))
    d2 = tk.Frame(tab2); d2.pack(fill=tk.X, pady=5)
    od2_var = tk.StringVar()
    tk.Entry(d2, textvariable=od2_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(d2, text="浏览...", command=lambda: od2_var.set(filedialog.askdirectory())).pack(side=tk.RIGHT, padx=(5,0))
    
    log2 = tk.Text(tab2, height=6, state=tk.DISABLED)
    log2.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def run2():
        try: r = int(row_var.get())
        except: messagebox.showerror("错误", "请输入有效的行数"); return
        s, m = split_excel_by_rows(f2_var.get(), r, od2_var.get())
        log2.config(state=tk.NORMAL); log2.insert(tk.END, m+"\n"); log2.config(state=tk.DISABLED)
        if s: messagebox.showinfo("完成", m)
    tk.Button(tab2, text="开始拆分", command=run2, bg="#4CAF50", fg="white").pack(pady=5)
    
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--column":
        s, m = split_excel_by_column(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ".")
        print(m)
    elif len(sys.argv) > 1 and sys.argv[1] == "--rows":
        s, m = split_excel_by_rows(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else ".")
        print(m)
    else:
        main()
