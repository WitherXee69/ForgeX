import time
from typing import final

import requests

class Fetcher:
    def __init__(self, settings, exception_handler):
        self.settings = settings
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.settings.git_token}"
        }
        self.exception_handler = exception_handler

    @final
    def validator(self, response):
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            return self.exception_handler.exception_unexpected_error(response.status_code, "Bad Request")
        elif response.status_code == 404:
            return self.exception_handler.exception_repo_not_found()
        elif response.status_code in (403, 429):
            body = {}
            try:
                body = response.json()
            except ValueError:
                pass

            message = body.get("message", "").lower()
            is_rate_limit = (
                    response.status_code == 429
                    or "rate limit" in message
                    or "abuse detection" in message
                    or response.headers.get("x-ratelimit-remaining") == "0"
            )

            if not is_rate_limit:
                return self.exception_handler.exception_unexpected_error(response.status_code, message)

            # 1. Check Retry-After header (common on 429 / secondary limits)
            if "retry-after" in response.headers:
                wait_seconds = int(response.headers["retry-after"])
                return self.exception_handler.exception_secondary_limit_exceeded(wait_seconds)

            # 2. Check Primary Rate Limit reset timestamp
            elif response.headers.get("x-ratelimit-remaining") == "0":
                reset_timestamp = int(response.headers.get("x-ratelimit-reset", 0))
                wait_seconds = max(reset_timestamp - int(time.time()), 1)
                return self.exception_handler.exception_primary_limit_exceeded(wait_seconds)

            else:
                return self.exception_handler.exception_secondary_limit_exceeded("60")  # Default wait time for secondary limits
        elif response.status_code == 401:
            return self.exception_handler.exception_invalid_token()
        elif response.status_code == 422:
            return self.exception_handler.exception_invalid_repo_name()
        elif response.status_code == 503:
            return self.exception_handler.exception_unexpected_error(response.status_code, "Service Unavailable")
        elif response.status_code == 500:
            return self.exception_handler.exception_unexpected_error(response.status_code, "Internal Server Error")
        elif response.status_code == 502:
            return self.exception_handler.exception_unexpected_error(response.status_code, "Bad Gateway")
        elif response.status_code == 504:
            return self.exception_handler.exception_unexpected_error(response.status_code, "Gateway Timeout")
        return None

    def fetch(self, owner, repo):
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            if self.validator(response):
                data = response.json()
                return data
            return None
        except requests.ConnectionError:
            return self.exception_handler.exception_no_internet_connection()

    def search(self, repo_name):
        try:
            url = f"https://api.github.com/search/repositories?q={repo_name}"
            response = requests.get(url, headers=self.headers)
            if self.validator(response):
                data = response.json()
                return data['items']
            return None
        except requests.ConnectionError:
            return self.exception_handler.exception_no_internet_connection()

    def fetch_latest_releases(self, owner, repo):
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(url, headers=self.headers)
            if self.validator(response):
                data = response.json()
                return data
            return None
        except requests.ConnectionError:
            return self.exception_handler.exception_no_internet_connection()

    def fetch_asset_content(self, asset_url):
        try:
            response = requests.get(asset_url, headers=self.headers)
            if self.validator(response):
                return response.content
            return None
        except requests.ConnectionError:
            return self.exception_handler.exception_no_internet_connection()