import os
import pandas as pd
from collections import Counter

def run_osa(folder_path):
    """
    OSA 数据分析函数
    - 直接读取传入文件夹路径
    """

    try:
        # 1. 获取文件夹路径
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])
        if not files:
            return "未找到 CSV 文件，请检查文件夹内容。"

        results = []
        device_count = Counter()

        # 2. 遍历文件
        for file in files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # 计算 Tone Count（非零数据个数）
            tone_count = (df.iloc[:, 1] > 0.2).sum()

            # 提取 device_id (第3-5段)
            parts = file.split('-')
            if len(parts) >= 5:
                device_id = f"{parts[2]}-{parts[4]}"
            else:
                device_id = parts[0]

            # 计数重复
            device_count[device_id] += 1

            # 解析器件类型
            if "-6-" in file:
                device_type = 6
            elif "-7-" in file:
                device_type = 7
            elif "-8-" in file:
                device_type = 8
            else:
                device_type = "Unknown"

            results.append([device_type, tone_count])

        # 转为 DataFrame
        result_df = pd.DataFrame(
            results,
            columns=["Device Type", "Tone Count"]
        )

        # 保存结果
        output_path = os.path.join(folder_path, "osa_summary.csv")
        result_df.to_csv(output_path, index=False)

        # 统计信息
        total_files = len(files)
        unique_devices = len(device_count)
        duplicates = {k: v for k, v in device_count.items() if v > 1}

        result_msg = f"分析完成！结果已保存至 osa_summary.csv\n总文件数：{total_files}，唯一器件数：{unique_devices}"
        if duplicates:
            result_msg += "\n重复测试的器件：\n"
            for device_id, count in duplicates.items():
                result_msg += f"- {device_id} 测试了 {count} 次\n"
        else:
            result_msg += "\n没有重复测试的器件。"

        return result_msg

    except Exception as e:
        return f"分析失败: {e}"