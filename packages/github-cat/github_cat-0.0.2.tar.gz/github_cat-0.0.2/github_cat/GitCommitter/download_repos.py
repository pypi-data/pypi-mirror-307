import os
import pandas as pd
import shutil


def move_file(src_folder, dst_folder, filename):
    """
    将指定的 txt 文件从一个文件夹移动到另一个文件夹。

    :param src_folder: 源文件夹的路径。
    :param dst_folder: 目标文件夹的路径。
    :param filename: 要移动的 txt 文件名。
    """
    # 拼接源文件的完整路径
    src_path = os.path.join(src_folder, filename)

    # 拼接目标文件的完整路径
    dst_path = os.path.join(dst_folder, filename)

    # 检查源文件是否存在
    if not os.path.exists(src_path):
        print(f"Error: Source file {src_path} does not exist.")
        return

    # 检查目标文件夹是否存在，如果不存在则创建它
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
        print(f"Created target directory: {dst_folder}")

    # 移动文件到目标文件夹
    try:
        shutil.move(src_path, dst_path)
        print(f"File {filename} moved from {src_folder} to {dst_folder} successfully.")
    except Exception as e:
        print(f"An error occurred while moving the file: {e}")

def save_txt_to_excel(input_file: str, output_file: str):
    """
    读取指定的输入文件，将数据提取为 Commits, Name, Email，并保存到 Excel 文件中。

    :param input_file: 要读取的输入文件路径 (txt 格式)。
    :param output_file: 要保存的输出文件路径 (xlsx 格式)。
    """
    try:
        # Step 1: 读取文件数据
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Step 2: 处理数据，提取 Commits, Name, Email
        data = []
        for line in lines:
            parts = line.split()
            commits = parts[0]
            email = parts[-1].strip('<>')  # 移除 email 周围的尖括号
            name = " ".join(parts[1:-1])    # 连接中间部分形成名字
            data.append({'Commits': commits, 'Name': name, 'Email': email})

        # Step 3: 将数据转换为 DataFrame
        df = pd.DataFrame(data)

        # Step 4: 将 DataFrame 写入 Excel 文件
        df.to_excel(output_file, index=False)

        print(f"Excel file created successfully as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# 示例调用
# save_to_excel('llvm.txt', 'llvm.xlsx')


folder = './shortlog'
# 如果文件夹不存在则创建
os.makedirs(folder, exist_ok=True)
dst_folder = os.path.abspath(folder)



def git_clone_and_shortlog(git_url):
    # 获取txt文件名
    txt_name = git_url.split("/")[-1] + ".txt"

    # 获取仓库名称
    repo_name = git_url.split("/")[-1]

    # repo_filename = git_url.split("/")[-2] + '_' + git_url.split("/")[-1]

    # 检查仓库目录是否已经存在
    if not os.path.exists(repo_name):
        # 克隆仓库
        os.system(f"git clone {git_url}")
    else:
        print(f"Repository {repo_name} already exists. Skipping clone.")


    # 进入仓库目录
    os.chdir(repo_name)

    # 生成shortlog文件
    os.system(f"git shortlog -sne --all > {txt_name}")

    # 把当前文件夹下的txt_name移动到folder中
    move_file(src_folder=os.getcwd(), dst_folder=dst_folder, filename=txt_name)

    # txt转化成excel
    os.chdir(dst_folder)
    save_txt_to_excel(txt_name, f"{repo_name}.xlsx")




