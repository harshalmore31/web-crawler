#!/usr/bin/env python3
import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from rich.style import Style
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from src.search import SearchEngine
from src.config import config

console = Console()

def create_header() -> Panel:
    """Create a header panel for the application"""
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row("[bold cyan]Web Content Analysis Tool[/bold cyan]")
    grid.add_row("[blue]Powered by Google Search & Gemini AI[/blue]")
    return Panel(grid, style="bold white")

def create_search_status(status: str) -> Panel:
    """Create a status panel"""
    return Panel(f"[bold yellow]{status}[/bold yellow]", title="Status", border_style="yellow")

async def interactive_search():
    """Run the interactive search interface"""
    try:
        # Clear screen and show header
        console.clear()
        console.print(create_header())
        console.print()

        # Get search query from user
        query = Prompt.ask("[bold cyan]Enter your search query[/bold cyan]")
        if not query.strip():
            console.print("[red]Error: Search query cannot be empty[/red]")
            return 1

        # Initialize search engine
        search_engine = SearchEngine()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="status", size=3),
            Layout(name="progress", size=3),
            Layout(name="results", ratio=1)
        )

        # Set up progress display
        progress_table = Table.grid(expand=True)
        progress_table.add_column(justify="left", ratio=1)
        
        # Create progress components
        search_progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green"),
            TimeRemainingColumn(),
            expand=True
        )
        
        with Live(layout, refresh_per_second=10, screen=True) as live:
            # Update header
            layout["header"].update(create_header())
            
            # Start search process
            layout["status"].update(create_search_status("Initializing search..."))
            
            try:
                # Perform search and get results
                with search_progress as progress:
                    task_id = progress.add_task("[cyan]Searching and analyzing...", total=None)
                    layout["progress"].update(Panel(search_progress))
                    
                    summary = await search_engine.search(query)
                    progress.update(task_id, completed=True)
                
                # Display results
                results_panel = Panel(
                    Markdown(summary),
                    title="[bold green]Analysis Results[/bold green]",
                    border_style="green"
                )
                layout["results"].update(results_panel)
                
                # Update status
                layout["status"].update(create_search_status("Search completed successfully!"))
                
                # Wait for user to read results
                console.input("\nPress Enter to exit...")
                
            except Exception as e:
                layout["status"].update(Panel(f"[bold red]Error: {str(e)}[/bold red]", 
                                            title="Error", border_style="red"))
                return 1
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Search interrupted by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        return 1
    
    return 0

def run():
    """Entry point for the application"""
    try:
        exit_code = asyncio.run(interactive_search())
        return exit_code
    except KeyboardInterrupt:
        console.print("\n[yellow]Program interrupted by user[/yellow]")
        return 1

if __name__ == "__main__":
    exit(run())