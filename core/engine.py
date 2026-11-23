from core.parser import parse_input

class Engine:
    def __init__(self, input_str, context, fetcher):
        self.input_str = input_str
        self.context = context
        self.fetcher = fetcher
        #self.resolver = resolver
        #self.installer = installer

    def handler(self):
        owner, repo = parse_input(self.input_str)

        if owner and repo:
            data = self.fetcher.fetch(owner, repo)
            if data:
                return {
                    "type": "single",
                    "data": data
                }
            else:
                return {
                    "type": "error",
                    "message": "Failed to fetch repository data."
                }
        else:
            repositories = self.fetcher.search(self.input_str)
            if repositories:
                return {
                    "type": "multiple",
                    "options": repositories
                }
            else:
                return {
                    "type": "error",
                    "message": "No repositories found."
                }