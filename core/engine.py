from core.parser import parse_input

class Engine:
    def __init__(self, context, fetcher):
        self.context = context
        self.fetcher = fetcher
        #self.resolver = resolver
        #self.installer = installer

    @staticmethod
    def _repository_summary(repo):
        license_info = repo.get("license") or {}
        return {
            "name": repo.get("name", "Unknown repository"),
            "full_name": repo.get("full_name", ""),
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language"),
            "license": license_info.get("spdx_id") or "Unknown",
            "version": repo.get("version"),
            "updated": repo.get("updated_at"),
            "tags": repo.get("tags", []),
        }

    def handler(self, input_str):
        owner, repo = parse_input(input_str)

        if owner and repo:
            data = self.fetcher.fetch(owner, repo)
            if not isinstance(data, dict):
                return {}
            return self._repository_summary(data)

        else:
            repositories = self.fetcher.search(input_str)
            if not isinstance(repositories, dict):
                return []
            repo_items = repositories.get("items", [])
            if not isinstance(repo_items, list):
                return []
            return [self._repository_summary(item) for item in repo_items]