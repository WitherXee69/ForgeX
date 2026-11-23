from urllib.parse import urlparse

def parse_github_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) >= 2 and parsed_url.netloc in ["github.com", "www.github.com"]:
        owner = path_parts[0]
        repo = path_parts[1]
        return owner, repo
    return ValueError("Invalid GitHub URL")

def parse_input(input_str):
    if input_str.startswith("http://") or input_str.startswith("https://"):
        return parse_github_url(input_str)
    elif "/" in input_str:
        owner, repo = input_str.split("/", 1)
        return owner.strip(), repo.strip()
    else:
        return None, input_str