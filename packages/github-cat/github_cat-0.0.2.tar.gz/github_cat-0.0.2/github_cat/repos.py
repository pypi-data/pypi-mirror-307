import requests
import random
import os
from typing import List, Optional

class GithubCrawler:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.base_url = "https://api.github.com"
        self.result_dir = './result'

        # Ensure the result directory exists
        os.makedirs(self.result_dir, exist_ok=True)

    def _get_headers(self) -> dict:
        """Selects a random token for authentication and returns headers."""
        token = random.choice(self.tokens)
        return {"Authorization": f"token {token}"}

    def _get_response(self, user: str, page: int) -> Optional[List[dict]]:
        """Attempts to fetch repositories for a given user and page, with retries on failure."""
        retries = 10
        for attempt in range(retries):
            try:
                url = f"{self.base_url}/orgs/{user}/repos?per_page=100&page={page}"
                response = requests.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException:
                print(f"Request failed. Retrying {attempt + 1}/{retries}...")
        return None

    def _save_results(self, user: str, repos: List[str]):
        """Saves the list of repository URLs to a file."""
        file_path = f"{self.result_dir}/{user}.txt"
        if os.path.exists(file_path):
            print(f"{file_path} already exists. Skipping save.")
            return

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(repos))
        print(f"Saved results to {file_path}")

    def crawl_user_repos(self, user: str):
        """Fetches all repositories of a given user and saves them."""
        print(f"Starting crawl for user: {user}")
        all_repos = []
        page = 1

        while True:
            repos = self._get_response(user, page)
            if repos is None or not repos:
                break

            all_repos.extend(repo['html_url'] for repo in repos)
            page += 1

        self._save_results(user, all_repos)
        print(f"Completed crawl for user: {user}")



