import os
import pandas as pd
import shutil

import git
from git import Repo
from git.remote import RemoteProgress

from colorama import init, Fore, Style

init(autoreset=True)

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        percentage = (cur_count / max_count) * 100
        progress_str = f"\r{Fore.RED}Progress: {message} | {percentage:.2f}%{Style.RESET_ALL}"
        if message:
            print(progress_str, end='', flush=True)

class GitRepoProcessor:
    """
    处理 Git 仓库相关操作的类，包含克隆仓库、生成 shortlog 文件、移动文件和保存为 Excel 文件的功能。
    """

    def __init__(self, git_url, output_folder='./shortlog'):
        """
        初始化 GitRepoProcessor 类。

        :param git_url: Git 仓库的 URL。
        :param output_folder: 保存输出文件的文件夹路径，默认为 './shortlog'。
        """
        self.git_url = git_url
        self.repo_name = git_url.split("/")[-1]
        self.repo_parent = git_url.split("/")[-2]
        self.txt_name = self.repo_name + ".txt"
        self.output_folder = os.path.abspath(output_folder + '/' + self.repo_parent)
        self.root_path = os.path.dirname(os.path.abspath(__file__))

        # 如果输出文件夹不存在，则创建
        os.makedirs(self.output_folder, exist_ok=True)

    def clone_repo(self):
        """
        克隆 Git 仓库。如果仓库已经存在，则跳过克隆操作。
        """
        if not os.path.exists(self.repo_name):
            os.system(f"git clone {self.git_url}")
        else:
            print(f"Repository {self.repo_name} already exists. Skipping clone.")

    def clone_repo_progress(self):
        """
        克隆 Git 仓库。如果仓库已经存在，则跳过克隆操作。
        显示克隆进度。
        """
        if not os.path.exists(self.repo_name):
            print(f"Cloning repository {self.repo_name} from {self.git_url}")
            try:
                Repo.clone_from(self.git_url, self.repo_name, progress=CloneProgress())
            except git.GitError as e:
                print(f"Error while cloning repository: {e}")
        else:
            print(f"Repository {self.repo_name} already exists. Skipping clone.")

    def generate_shortlog(self):
        """
        生成 shortlog 文件并保存到仓库目录中。
        """
        os.chdir(self.repo_name)
        print(f"\nGenerating shortlog for {self.repo_name}")
        os.system(f"git shortlog -sne --all > {self.txt_name}")


    def move_file_to_output(self):
        """
        将生成的 shortlog 文件移动到输出文件夹中。
        """
        move_file(src_folder=os.getcwd(), dst_folder=self.output_folder, filename=self.txt_name)

    def save_to_excel(self):
        """
        将 shortlog 文件的数据提取为 Commits, Name, Email，并保存为 Excel 文件。
        """
        os.chdir(self.output_folder)
        save_txt_to_excel(self.txt_name, f"{self.repo_name}.xlsx")

    def clean_up(self):
        """
        删除 repo_name 文件夹及其所有内容。
        """
        os.chdir(self.root_path)
        if os.path.exists(self.repo_name):
            os.system(f'rmdir /S /Q {self.repo_name}')
            print(f"Repository directory {self.repo_name} has been removed.")

    def check_file(self):
        """
        检查输出文件夹中是否存在同名文件。
        """
        if os.path.exists(os.path.join(self.output_folder, f"{self.repo_name}.xlsx")):
            print(f"{self.repo_name}.xlsx already exists. Skipping...")
            return True
        return False

    def run(self):
        """
        执行完整的处理流程：克隆仓库 -> 生成 shortlog -> 移动文件 -> 保存为 Excel 文件 -> 清理工作目录。
        """
        if self.check_file():
            return
        # self.clone_repo()
        self.clone_repo_progress()
        self.generate_shortlog()
        self.move_file_to_output()
        self.save_to_excel()
        self.clean_up()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean_up()


def move_file(src_folder, dst_folder, filename):
    """
    将指定的文件从一个文件夹移动到另一个文件夹。

    :param src_folder: 源文件夹的路径。
    :param dst_folder: 目标文件夹的路径。
    :param filename: 要移动的文件名。
    """
    src_path = os.path.join(src_folder, filename)
    dst_path = os.path.join(dst_folder, filename)

    if not os.path.exists(src_path):
        print(f"Error: Source file {src_path} does not exist.")
        return

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
        print(f"Created target directory: {dst_folder}")

    try:
        shutil.move(src_path, dst_path)
        print(f"{filename} moved from {src_folder} to {dst_folder} successfully.")
    except Exception as e:
        print(f"An error occurred while moving the file: {e}")


def save_txt_to_excel(input_file: str, output_file: str):
    """
    读取指定的输入文件，将数据提取为 Commits, Name, Email，并保存到 Excel 文件中。

    :param input_file: 要读取的输入文件路径 (txt 格式)。
    :param output_file: 要保存的输出文件路径 (xlsx 格式)。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        data = []
        for line in lines:
            parts = line.split()
            commits = parts[0]
            email = parts[-1].strip('<>')
            name = " ".join(parts[1:-1])
            data.append({'Commits': commits, 'Name': name, 'Email': email})

        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)

        print(f"Excel file created successfully as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_file_to_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


import concurrent.futures


def process_repo(url, timeout=60*20):
    print(f"Processing: {url}")
    processor = GitRepoProcessor(url)

    # 使用线程池执行processor.run()并设置超时时间
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future = executor.submit(processor.run)
        try:
            future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print(f"Timeout: Skipping {url}")


def main(file_path):
    urls = read_file_to_list(file_path)
    exclude_urls = read_file_to_list('./files/exclude_urls.txt')

    for url in urls:
        if url in exclude_urls:
            print(f"Skipping {url}")
            continue
        process_repo(url)



