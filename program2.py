# -*- codeing = utf-8 -*-
# @Time : 2023/11/29 3:19 下午
# @Author : Li Qing
# @File : program2.py
# @Software : PyCharm
import os
import csv

def split_and_save_batches(csv_file_path, batch_size, output_folder='output'):
    # 存储所有数据的列表
    data_list = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 跳过标题行
        next(reader, None)
        # 将每一行数据添加到列表
        for row in reader:
            data_list.append(row)

    # 按照指定批次大小拆分列表
    batches = [data_list[i:i + batch_size] for i in range(0, len(data_list), batch_size)]

    # 创建输出文件夹
    output_folder_path = output_folder
    os.makedirs(output_folder_path, exist_ok=True)

    # 保存每个批次为 txt 文件
    for i, batch in enumerate(batches, start=1):
        output_file_path = f"{output_folder_path}/batch_{i}.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for row in batch:
                output_file.write(','.join(row) + '\n')

        print(f"Batch {i} - Length: {len(batch)} - Saved to: {output_file_path}")

def main():
    # CSV文件路径、批次大小和输出文件夹
    csv_file_path = 'fyx_chinamoney.csv'
    batch_size = 80
    output_folder = 'output'

    # 调用拆分和保存函数
    split_and_save_batches(csv_file_path, batch_size, output_folder)

# if __name__ == "__main__":
#     main()

