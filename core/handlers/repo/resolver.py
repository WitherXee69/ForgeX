class Resolver:
    def __init__(self, context, fetcher, validator):
        self.context = context
        self.fetcher = fetcher
        self.validator = validator

    def resolver(self):
        releases = self.fetcher.fetch_releases(self.context.repo_data['owner']['login'], 
                                               self.context.repo_data['name'])

        if releases:
            assets = releases.get('assets', [])
            if assets:
                for asset in assets:
                    if ".forgeman" in asset['name']:
                        manifest_content = self.fetcher.fetch_asset_content(asset['url'])
                        if manifest_content:
                            self.validator.validate(manifest_content)