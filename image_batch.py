#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量图片处理工具 - 压缩、缩放、格式转换、加水印"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def batch_resize(input_dir, output_dir, width=None, height=None, quality=85, fmt=None):
    """批量调整图片大小"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    exts = {'.jpg','.jpeg','.png','.gif','.bmp','.webp','.tiff'}
    files = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in exts]
    
    if not files: return False, "未找到图片文件"
    
    processed = 0
    for f in files:
        try:
            img = Image.open(f)
            if width and height:
                img = img.resize((width, height), Image.LANCZOS)
            elif width:
                ratio = width / img.width
                img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
            elif height:
                ratio = height / img.height
                img = img.resize((int(img.width * ratio), height), Image.LANCZOS)
            
            out_fmt = fmt.lower() if fmt else f.suffix[1:]
            out_path = Path(output_dir) / f"{f.stem}.{out_fmt}"
            save_kwargs = {'quality': quality} if out_fmt in ('jpg','jpeg','webp') else {}
            img.save(out_path, format=out_fmt.upper() if fmt else None, **save_kwargs)
            processed += 1
        except Exception as e:
            print(f"处理 {f.name} 失败: {e}")
    
    return True, f"成功处理 {processed}/{len(files)} 个文件"


def batch_compress(input_dir, output_dir, quality=60):
    """批量压缩图片"""
    return batch_resize(input_dir, output_dir, quality=quality)


def batch_convert(input_dir, output_dir, target_format='png'):
    """批量转换格式"""
    return batch_resize(input_dir, output_dir, fmt=target_format)


def batch_watermark(input_dir, output_dir, watermark_text="Watermark", position="右下"):
    """批量添加水印"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    exts = {'.jpg','.jpeg','.png','.gif','.bmp','.webp'}
    files = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in exts]
    
    if not files: return False, "未找到图片文件"
    
    positions = {"左上": (10,10), "右上": (None,10), "左下": (10,None), "右下": (None,None), "居中": ("center","center")}
    pos = positions.get(position, (None,None))
    
    processed = 0
    for f in files:
        try:
            img = Image.open(f).convert("RGBA")
            txt_layer = Image.new("RGBA", img.size, (255,255,255,0))
            draw = ImageDraw.Draw(txt_layer)
            
            try:
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0,0), watermark_text, font=font)
            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
            
            x = pos[0] if pos[0] not in (None, "center") else (img.width-tw)//2
            y = pos[1] if pos[1] not in (None, "center") else (img.height-th)//2
            if pos[0] is None: x = img.width - tw - 10
            if pos[1] is None: y = img.height - th - 10
            
            draw.text((x,y), watermark_text, font=font, fill=(255,255,255,120))
            watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
            watermarked.save(Path(output_dir) / f.name, quality=95)
            processed += 1
        except Exception as e:
            print(f"处理 {f.name} 失败: {e}")
    
    return True, f"成功处理 {processed}/{len(files)} 个文件"


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    
    root = tk.Tk()
    root.title("批量图片处理工具")
    root.geometry("600x500")
    root.resizable(False, False)
    
    tk.Label(root, text="批量图片处理工具", font=("", 16, "bold")).pack(pady=10)
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def make_tab(parent, run_fn):
        tk.Label(parent, text="输入目录:").pack(anchor=tk.W, pady=(10,0))
        f1 = tk.Frame(parent); f1.pack(fill=tk.X, pady=5)
        iv = tk.StringVar()
        tk.Entry(f1, textvariable=iv).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(f1, text="浏览...", command=lambda: iv.set(filedialog.askdirectory())).pack(side=tk.RIGHT)
        
        tk.Label(parent, text="输出目录:").pack(anchor=tk.W, pady=(5,0))
        f2 = tk.Frame(parent); f2.pack(fill=tk.X, pady=5)
        ov = tk.StringVar()
        tk.Entry(f2, textvariable=ov).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(f2, text="浏览...", command=lambda: ov.set(filedialog.askdirectory())).pack(side=tk.RIGHT)
        
        log = tk.Text(parent, height=6, state=tk.DISABLED)
        log.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def cb():
            s, m = run_fn(iv.get(), ov.get())
            log.config(state=tk.NORMAL); log.insert(tk.END, m+"\n"); log.config(state=tk.DISABLED)
            if s: messagebox.showinfo("完成", m)
        
        tk.Button(parent, text="开始处理", command=cb, bg="#4CAF50", fg="white").pack(pady=5)
        return iv, ov
    
    t1 = tk.Frame(notebook); notebook.add(t1, text="缩放")
    tk.Label(t1, text="宽度:").pack(anchor=tk.W, padx=10)
    wv = tk.StringVar(value="800")
    tk.Entry(t1, textvariable=wv).pack(fill=tk.X, padx=10)
    tk.Label(t1, text="高度(留空自动比例):").pack(anchor=tk.W, padx=10, pady=(5,0))
    hv = tk.StringVar()
    tk.Entry(t1, textvariable=hv).pack(fill=tk.X, padx=10)
    i1, o1 = make_tab(t1, lambda i, o: batch_resize(i, o, int(wv.get()) if wv.get().isdigit() else None, int(hv.get()) if hv.get().isdigit() else None))
    
    t2 = tk.Frame(notebook); notebook.add(t2, text="压缩")
    tk.Label(t2, text="质量(1-100):").pack(anchor=tk.W, padx=10, pady=(5,0))
    qv = tk.StringVar(value="60")
    tk.Entry(t2, textvariable=qv).pack(fill=tk.X, padx=10)
    i2, o2 = make_tab(t2, lambda i, o: batch_compress(i, o, int(qv.get()) if qv.get().isdigit() else 60))
    
    t3 = tk.Frame(notebook); notebook.add(t3, text="加水印")
    tk.Label(t3, text="水印文字:").pack(anchor=tk.W, padx=10, pady=(5,0))
    wtv = tk.StringVar(value="Watermark")
    tk.Entry(t3, textvariable=wtv).pack(fill=tk.X, padx=10)
    i3, o3 = make_tab(t3, lambda i, o: batch_watermark(i, o, wtv.get()))
    
    root.mainloop()


if __name__ == "__main__":
    main()
