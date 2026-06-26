#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF报表生成工具 - 从数据生成专业PDF报表"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Try to register Chinese fonts
_FONT_NAME = 'Helvetica'
for font_path in ['/System/Library/Fonts/PingFang.ttc',
                  '/System/Library/Fonts/STHeiti Light.ttc',
                  '/System/Library/Fonts/Hiragino Sans GB.ttc',
                  'C:/Windows/Fonts/simsun.ttc',
                  'C:/Windows/Fonts/msyh.ttc']:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('CJK', font_path))
            _FONT_NAME = 'CJK'
            break
        except:
            pass


def create_report(output_file, title, data_rows, headers=None, subtitle=""):
    """
    从数据生成PDF报表
    
    Args:
        output_file: 输出PDF路径
        title: 报表标题
        data_rows: 数据行列表，每行是一个列表
        headers: 表头列表
        subtitle: 副标题
    """
    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
                                  fontName=_FONT_NAME, fontSize=22, spaceAfter=6)
    sub_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                                fontName=_FONT_NAME, fontSize=11, textColor=colors.grey)
    normal = ParagraphStyle('Normal', fontName=_FONT_NAME, fontSize=10, spaceAfter=4)
    header_style = ParagraphStyle('Header', fontName=_FONT_NAME, fontSize=10,
                                   textColor=colors.white, alignment=1)
    
    elements = []
    elements.append(Paragraph(title, title_style))
    if subtitle:
        elements.append(Paragraph(subtitle, sub_style))
    elements.append(Spacer(1, 12))
    
    if headers and data_rows:
        table_data = [headers] + data_rows
        col_count = len(headers)
        col_widths = [doc.width / col_count] * col_count
        
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), _FONT_NAME),
            ('FONTNAME', (0,1), (-1,-1), _FONT_NAME),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ])
        table.setStyle(style)
        elements.append(table)
    elif data_rows:
        for row in data_rows:
            elements.append(Paragraph(str(row), normal))
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
                               ParagraphStyle('Footer', fontName=_FONT_NAME, fontSize=8, textColor=colors.grey)))
    
    doc.build(elements)
    return True, f"PDF报表已生成: {output_file}"


def create_invoice_report(output_file, company_name, items, tax_rate=0.13):
    """生成报价单/发票报表"""
    headers = ['序号', '项目', '数量', '单价(¥)', '金额(¥)']
    total = 0
    data_rows = []
    for i, item in enumerate(items, 1):
        name, qty, price = item[0], item[1], item[2]
        amount = qty * price
        total += amount
        data_rows.append([str(i), name, str(qty), f"{price:.2f}", f"{amount:.2f}"])
    
    tax = total * tax_rate
    grand_total = total + tax
    
    data_rows.append(['', '', '', '小计:', f"{total:.2f}"])
    data_rows.append(['', '', '', f'税金({tax_rate*100:.0f}%):', f"{tax:.2f}"])
    data_rows.append(['', '', '', '合计:', f"{grand_total:.2f}"])
    
    return create_report(output_file, f"{company_name} - 报价单", data_rows, headers)


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    
    root = tk.Tk()
    root.title("PDF报表生成工具")
    root.geometry("500x400")
    root.resizable(False, False)
    
    tk.Label(root, text="PDF报表生成工具", font=("", 16, "bold")).pack(pady=10)
    
    tk.Label(root, text="报表标题:").pack(anchor=tk.W, padx=20, pady=(5,0))
    t_var = tk.StringVar(value="数据分析报表")
    tk.Entry(root, textvariable=t_var).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Label(root, text="副标题:").pack(anchor=tk.W, padx=20, pady=(5,0))
    s_var = tk.StringVar(value="由办公自动化工具箱生成")
    tk.Entry(root, textvariable=s_var).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Label(root, text="表头(逗号分隔):").pack(anchor=tk.W, padx=20, pady=(5,0))
    h_var = tk.StringVar(value="序号,项目,数值,备注")
    tk.Entry(root, textvariable=h_var).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Label(root, text="数据行数:").pack(anchor=tk.W, padx=20, pady=(5,0))
    r_var = tk.StringVar(value="10")
    tk.Entry(root, textvariable=r_var).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Label(root, text="输出文件:").pack(anchor=tk.W, padx=20, pady=(5,0))
    f1 = tk.Frame(root); f1.pack(fill=tk.X, padx=20, pady=5)
    o_var = tk.StringVar(value="报表.pdf")
    tk.Entry(f1, textvariable=o_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(f1, text="选择...", command=lambda: o_var.set(filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF文件","*.pdf")]))).pack(side=tk.RIGHT, padx=(5,0))
    
    log_text = tk.Text(root, height=4, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    
    def run():
        headers = [h.strip() for h in h_var.get().split(',') if h.strip()]
        try: rows_count = int(r_var.get())
        except: rows_count = 10
        
        data_rows = [[str(j), f"示例数据_{j}", f"{j*10}", f"备注{j}"] for j in range(1, rows_count+1)]
        
        s, m = create_report(o_var.get(), t_var.get(), data_rows, headers, s_var.get())
        log_text.config(state=tk.NORMAL); log_text.insert(tk.END, m+"\n"); log_text.config(state=tk.DISABLED)
        if s: messagebox.showinfo("完成", m)
    
    tk.Button(root, text="生成PDF报表", command=run, bg="#4CAF50", fg="white", font=("", 12, "bold")).pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()
