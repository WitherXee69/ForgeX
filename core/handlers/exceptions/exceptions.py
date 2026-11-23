from typing import final


class FX_ExceptionHandler:
    # GitHub API exception handler
    @final
    def exception_invalid_token(self):
        return f"[red]Invalid GitHub token. Please check your token and try again.[/red]"
    @final
    def exception_primary_limit_exceeded(self, reset_time):
        return (f"[red]Primary rate limit exceeded. Please try again in[/red] [green]{reset_time}[/green] [red]seconds. "
                f"Or try using your authentication token.[/red]")
    @final
    def exception_secondary_limit_exceeded(self, wait_time):
        return (f"[red]Secondary rate limit exceeded. Please try again in[/red] [green]{wait_time}[/green] [red]seconds. "
                f"Or try using your authentication token.[/red]")


    @final
    def exception_no_internet_connection(self):
        return f"[red]No Internet Connection. Please check your network settings and try again.[/red]"


    # Repository exception handler
    @final
    def exception_invalid_repo_name(self):
        return f"[red]Invalid repository name. Please check the name and try again.[/red]"
    @final
    def exception_repo_not_found(self):
        return f"[red]Repository not found. Please check the name and try again.[/red]"
    @final
    def exception_owner_not_found(self):
        return f"[red]Owner not found. Please check the owner name and try again.[/red]"


    # Unexpected error handler
    @final
    def exception_unexpected_error(self, status_code, message):
        return f"[red]Unexpected error occurred. Status code: {status_code}, Message: {message}[/red]"
