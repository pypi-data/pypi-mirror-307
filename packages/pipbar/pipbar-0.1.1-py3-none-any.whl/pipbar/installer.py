import subprocess
import time
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.console import Console
from rich.text import Text

console = Console()

ASCII_ART = """
┏┓┳┏┓  ┳┓┏┓┳┓
┃┃┃┃┃  ┣┫┣┫┣┫
┣┛┻┣┛  ┻┛┛┗┛┗
"""

DEVELOPER_CREDIT = """
This project is open-source and contributed by [bold blue]Jiyath Khan[/bold blue].
Visit [bold green]https://github.com/Jiyath5516F/pip-bar[/bold green] to learn more.
"""

POSSIBLE_SOLUTIONS = {
    "permission denied": "Try running the command with `sudo` or as an administrator.",
    "network": "Check your internet connection or try again later.",
    "pip": "You may need to upgrade pip: `python -m pip install --upgrade pip`.",
    "dependency": "Try installing the missing dependencies manually.",
    "invalid": "Ensure the package name is correct and available on PyPI."
}

def get_error_message(stderr):
    """Analyze stderr and return a possible solution."""
    for error, solution in POSSIBLE_SOLUTIONS.items():
        if error.lower() in stderr.lower():
            return f"[red]Error: {error.capitalize()}[/red]\nPossible solution: {solution}"
    return "[red]Unknown error occurred during installation.[/red]"

def install_package(package_name: str):
    """Install a single package with a rich progress bar showing ETA, download speed, and developer credit."""
    
    console.print(ASCII_ART, style="bold cyan")
    console.print(DEVELOPER_CREDIT)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.fields[package]}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Installing...", package=package_name, total=100)
        
        try:
            process = subprocess.Popen(
                ["pip", "install", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            start_time = time.time()
            for i in range(1, 101):
                time.sleep(0.05)
                progress.update(task, advance=1)
                
                elapsed_time = time.time() - start_time
                progress_speed = i / elapsed_time if elapsed_time > 0 else 0
                progress.update(task, speed=progress_speed)

            stdout, stderr = process.communicate()

            process.wait()
            
            if process.returncode == 0:
                console.print(f"[green]✔ {package_name} installed successfully![/green]")
            else:
                error_message = get_error_message(stderr)
                console.print(f"[red]✖ Failed to install {package_name}[/red]")
                console.print(error_message)
        
        except Exception as e:
            console.print(f"[red]An error occurred: {e}[/red]")

def install_packages(packages):
    """Install multiple packages in sequence."""
    for package in packages:
        install_package(package)
