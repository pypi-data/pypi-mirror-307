import os
import pandas as pd
from glob import glob


def merge_excel_files(input_folder, output_file):
    # 获取 input_folder 的最后一个文件夹名
    folder_name = os.path.basename(input_folder.rstrip(os.sep))

    # 拼接 output_file 的路径
    output_file = os.path.join(output_folder, f'{folder_name}_merged_output.xlsx')

    # 如果 output 文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有 Excel 文件路径
    excel_files = glob(os.path.join(input_folder, '*.xlsx'))

    # 用于存储每个文件的 DataFrame
    dfs = []

    # 逐个处理文件
    for file in excel_files:
        # 获取文件名（不包含后缀）
        filename = os.path.splitext(os.path.basename(file))[0]

        # 读取 Excel 文件
        df = pd.read_excel(file)

        # 增加一列 'repo'，值为文件名
        df['repo'] = filename

        # 将 DataFrame 加入列表
        dfs.append(df)

    # 合并所有 DataFrame
    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)

        # 输出到 Excel 文件
        merged_df.to_excel(output_file, index=False)
        print(f'数据已成功合并并保存到 {output_file}')
    else:
        print('没有找到 Excel 文件')


