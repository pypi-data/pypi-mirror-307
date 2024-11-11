# Introduction
## Install package
```shell
pip install github_bird
```

##  Example Usage:

```python
from github_cat.repos import GithubCrawler

# Define the GitHub API tokens here
tokens = ["your_token_1", "your_token_2"]  # Replace with actual tokens

crawler = GithubCrawler(tokens)
crawler.crawl_user_repos('milvus-io')

```
