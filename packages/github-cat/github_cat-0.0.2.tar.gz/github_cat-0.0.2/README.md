# Introduction
## Install package
```shell
pip install github_cat
```

##  Example Usage:

```python
from github_cat.repos import GithubCrawler

# Define the GitHub API tokens here
tokens = ["your_token_1", "your_token_2"]  # Replace with actual tokens

crawler = GithubCrawler(tokens)
crawler.crawl_user_repos('milvus-io')

```

```python
# GitCommitter.excel_process
from github_cat.GitCommitter import excel_process
input_folder = r'./shortlog/google'
output_folder = './output'
excel_process.merge_excel_files(input_folder, output_folder)


from github_cat.GitCommitter import download_repos
git_url = "https://github.com/dockur/macos"
download_repos.git_clone_and_shortlog(git_url)


from github_cat.GitCommitter import git_processor
# def main(file_path):
#     urls = read_file_to_list(file_path)
#     exclude_urls = read_file_to_list('./files/exclude_urls.txt')
# 
#     for url in urls:
#         if url in exclude_urls:
#             print(f"Skipping {url}")
#             continue
#         process_repo(url)

git_processor.main('./files/vector.txt')
    
urls = git_processor.read_file_to_list('./files/test.txt')
for url in urls:
    print(url)
    processor = git_processor.GitRepoProcessor(url)
    processor.run()


# 示例用法
git_url = "https://github.com/test/test"
processor = git_processor.GitRepoProcessor(git_url)
processor.run()

```