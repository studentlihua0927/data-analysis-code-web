import tkinter as tk
from tkinter import messagebox
from liv_analysis import run_liv
from osa_analysis import run_osa

def run_liv_analysis():
    """调用 LIV 分析函数"""
    result = run_liv(debug_mode=False)  # 非调试模式，弹出选择框
    messagebox.showinfo("LIV 分析结果", result)

def run_osa_analysis():
    """调用 OSA 分析函数"""
    result = run_osa(debug_mode=False)  # 非调试模式，弹出选择框
    messagebox.showinfo("OSA 分析结果", result)

# 创建主窗口
app = tk.Tk()
app.title("数据分析工具")
app.geometry("400x200")

# 标题
label = tk.Label(app, text="请选择要进行的分析类型", font=("Arial", 14))
label.pack(pady=20)

# LIV 按钮
btn_liv = tk.Button(app, text="运行 LIV 分析", width=20, height=2, command=run_liv_analysis)
btn_liv.pack(pady=10)

# OSA 按钮
btn_osa = tk.Button(app, text="运行 OSA 分析", width=20, height=2, command=run_osa_analysis)
btn_osa.pack(pady=10)

# 运行主循环
app.mainloop()