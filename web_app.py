import streamlit as st
import pandas as pd
import tempfile
import os

# 导入你现有的分析函数（已去掉 debug_mode 参数）
from liv_analysis import run_liv
from osa_analysis import run_osa

st.title("QD 数据分析网页工具")
st.write("直接上传 CSV 文件后选择分析类型，结果会在页面显示并生成 summary.csv 文件。")

# 1. 上传文件（多文件）
uploaded_files = st.file_uploader(
    "请拖入或选择多个 CSV 文件（支持多选）",  # 提示
    accept_multiple_files=True,
    type=["csv"]  # 只接受 csv 文件
)

# 2. 选择分析类型
analysis_type = st.radio(
    "选择分析类型",
    ("LIV 分析", "OSA 分析")
)

# 3. 运行分析按钮
if st.button("开始分析"):
    if not uploaded_files:
        st.error("请先上传 CSV 文件！")
    else:
        # 创建临时文件夹存储上传文件
        with tempfile.TemporaryDirectory() as tmpdirname:
            # 将所有上传的文件保存到临时文件夹
            for uploaded_file in uploaded_files:
                file_path = os.path.join(tmpdirname, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # 调用对应分析函数
            if analysis_type == "LIV 分析":
                result_msg = run_liv(tmpdirname)  # 去掉 debug_mode
                summary_path = os.path.join(tmpdirname, "liv_summary.csv")
            else:
                result_msg = run_osa(tmpdirname)  # 去掉 debug_mode
                summary_path = os.path.join(tmpdirname, "osa_summary.csv")

            # 显示结果
            st.success(result_msg)

            # 提供下载 summary.csv
            if os.path.exists(summary_path):
                with open(summary_path, "rb") as f:
                    st.download_button(
                        label="下载结果 CSV",
                        data=f,
                        file_name=os.path.basename(summary_path),
                        mime="text/csv"
                    )