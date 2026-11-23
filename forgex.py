import os
import shutil

from core.englne import Engine
from core.handlers.repo import Fetcher
from core.context import Context

from config.settings import Settings

from ui.cli import frontend_cli
from ui.renderer import Renderer

renderer = Renderer()
context = Context()
settings = Settings()

def forgex():
    fetcher = Fetcher(settings)
    
    while True:
        if settings.git_username is None and settings.git_token is None:
            # Get GitHub credentials from the user
            settings.git_username = frontend_cli("\nEnter your GitHub username: ", renderer)
            settings.git_token = frontend_cli("\nEnter your GitHub token: ", renderer)

        else:
            user_input = frontend_cli("\nEnter the repo name: ", renderer)
            current_input = user_input
            engine = Engine(current_input, context, fetcher)
            result = engine.handler()
            
            if result["type"] == "single":
                data = result["data"]
                renderer.render_out(f"\n[green]Repository:[/green] {data['full_name']}", "left")
                renderer.render_out(f"[green]Description:[/green] {data['description']}", "left")
                renderer.render_out(f"[green]Stars:[/green] {data['stargazers_count']}", "left")
                renderer.render_out(f"[green]Forks:[/green] {data['forks_count']}\n", "left")
            
                context.repo_data = data
                break
            
            elif result["type"] == "multiple":
                options = result["options"]
            
                renderer.render_out("\nSearch Results:\n", "left")
            
                for i, repo in enumerate(options, 1):
                    renderer.render_out(f"{i}. {repo['full_name']}", "left")
            
                choice = int(renderer.render_input("\nSelect a repo: "))
                current_input = options[choice - 1]["full_name"]
            
            
            elif result["type"] == "error":
                renderer.render_out(result["message"], "left")
                break

if __name__ == '__main__':
    try:
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        width = shutil.get_terminal_size().columns

        renderer.render_out("""\n
███████╗ ██████╗ ██████╗  ██████╗ ███████╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗   ╚███╔╝ 
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝   ██╔██╗ 
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██╔╝ ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                          """, justify="center")
        renderer.render_out("[i][reverse]Automated GitHub repo installer[/reverse][/i]\n", justify="center")
        renderer.render_out("-" * width, "center")
        renderer.render_out(">>>Enter the repo name you want to install<<<\n", "center")
        renderer.render_out("Ex:- [#3B78FF]WitherXee69/ForgeX[/#3B78FF] \n https://github.com/WitherXee69/ForgeX\n",
                            "center")
        renderer.render_out(
            ">>>If you dont know the username enter the repo_name and ForgeX will find you similar repos<<<", "center")
        renderer.render_out("-" * width, "center")
        while True:
            forgex()
    except KeyboardInterrupt:
        pass