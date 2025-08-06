import os
import pandas as pd
from collections import Counter

def run_liv(folder_path):
    """
    LIV 数据分析函数
    - 直接读取传入文件夹路径
    """

    try:
        # 1. 获取文件夹路径
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])
        if not files:
            return "未找到 CSV 文件，请检查文件夹内容。"

        latest_results = {}
        device_count = Counter()

        # 2. 遍历文件
        for file in files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # 只筛选电压列第一行在 -0.1 ~ 0.1 范围内的文件
            try:
                voltage_first = float(df.iloc[0, 1])
            except Exception:
                continue

            if not (-0.1 <= voltage_first <= 0.1):
                continue

            # 转换数值类型
            current = pd.to_numeric(df.iloc[:, 0], errors='coerce')  # 电流 (mA)
            power = pd.to_numeric(df.iloc[:, 2], errors='coerce')    # 功率 (mW)

            # 提取 device_id (第3-5段)
            parts = file.split('-')
            if len(parts) >= 5:
                device_id = f"{parts[2]}-{parts[4]}"
            else:
                device_id = parts[0]

            # 计数重复
            device_count[device_id] += 1

            # 阈值电流
            threshold_idx = power[power > 0.2].index.min()
            threshold_current = current.iloc[threshold_idx] if pd.notna(threshold_idx) else None

            # 150 mA 时功率
            power_150 = power[current == 150].values[0] if 150 in current.values else None

            # 判断死活
            is_dead = False
            if threshold_current is None or threshold_current > 130:
                is_dead = True
            if power_150 is None or power_150 < 1:
                is_dead = True

            if is_dead:
                threshold_current = f"{device_id} 器件已死"
                power_150 = f"{device_id} 器件已死"

            # 解析器件类型
            if "-6-" in file:
                device_type = 6
            elif "-7-" in file:
                device_type = 7
            elif "-8-" in file:
                device_type = 8
            else:
                device_type = "Unknown"

            # 保存最新结果
            latest_results[device_id] = [device_type, threshold_current, power_150]

        # 转为 DataFrame 并处理已死器件排序
        result_df = pd.DataFrame(
            list(latest_results.values()),
            columns=["Device Type", "Threshold Current (mA)", "Power at 150 mA (mW)"]
        )

        def is_dead_row(row):
            return "器件已死" in str(row["Threshold Current (mA)"]) or "器件已死" in str(row["Power at 150 mA (mW)"])

        alive_df = result_df[~result_df.apply(is_dead_row, axis=1)]
        dead_df = result_df[result_df.apply(is_dead_row, axis=1)]

        final_df = pd.concat([alive_df, dead_df], ignore_index=True)

        # 保存结果
        output_path = os.path.join(folder_path, "liv_summary.csv")
        final_df.to_csv(output_path, index=False)

        # 统计信息
        total_files = len(files)
        unique_devices = len(latest_results)
        dead_count = len(dead_df)
        alive_count = len(alive_df)

        duplicates = {k: v for k, v in device_count.items() if v > 1}

        # 生成结果字符串
        result_msg = f"分析完成！结果已保存至 liv_summary.csv\n总文件数：{total_files}，唯一器件数：{unique_devices}，正常器件：{alive_count}，已死器件：{dead_count}"
        if duplicates:
            result_msg += "\n重复测试的器件：\n"
            for device_id, count in duplicates.items():
                result_msg += f"- {device_id} 测试了 {count} 次\n"
        else:
            result_msg += "\n没有重复测试的器件。"

        return result_msg

    except Exception as e:
        return f"分析失败: {e}"