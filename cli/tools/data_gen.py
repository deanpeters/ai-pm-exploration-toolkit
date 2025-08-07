#!/usr/bin/env python3
"""
AI PM Toolkit - CLI Data Generation Tool
Beautiful command-line interface for synthetic data generation
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

# Add shared directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.text import Text
    from rich.layout import Layout
except ImportError:
    print("❌ Rich library not found. Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.text import Text
    from rich.layout import Layout

from data_generator import generate_sample_data, DataGenerator, PersonaConfig

console = Console()

class CLIDataGenerator:
    """CLI interface for data generation with rich output"""
    
    def __init__(self):
        self.generator = DataGenerator()
        self.working_dir = Path.cwd()
    
    def show_header(self):
        """Display the tool header"""
        title = Text("🎭 Synthetic Data Generation", style="bold cyan")
        subtitle = Text("Generate realistic user personas for product validation", style="dim")
        
        header_panel = Panel(
            Text.assemble(title, "\n", subtitle),
            box=box.DOUBLE,
            padding=(1, 2),
            style="cyan"
        )
        
        console.print(header_panel)
        console.print()
    
    def select_experience(self) -> str:
        """Let user select experience type"""
        console.print("[bold]Choose your learning experience:[/bold]")
        console.print()
        
        experiences = {
            "1": ("just_do_it", "🚀 Just Do It", "Generate data right now"),
            "2": ("learn_and_do", "🎓 Learn & Do", "Understand the process while doing it"),
            "3": ("cli_deep_dive", "🔧 CLI Deep Dive", "Master advanced data generation")
        }
        
        for key, (exp_id, name, desc) in experiences.items():
            console.print(f"{key}. {name}")
            console.print(f"   {desc}")
            console.print()
        
        choice = Prompt.ask("Select experience", choices=list(experiences.keys()), default="1")
        return experiences[choice][0]
    
    def configure_generation(self, experience_type: str) -> dict:
        """Configure generation parameters based on experience"""
        config = {}
        
        if experience_type == "just_do_it":
            config = self._quick_config()
        elif experience_type == "learn_and_do":
            config = self._learning_config()
        else:  # cli_deep_dive
            config = self._advanced_config()
        
        return config
    
    def _quick_config(self) -> dict:
        """Quick configuration for Just Do It experience"""
        console.print("[bold green]🚀 Quick Generation Setup[/bold green]")
        
        count = IntPrompt.ask("Number of personas", default=10, show_default=True)
        
        console.print("\nPersona types:")
        console.print("1. B2B SaaS Professionals")
        console.print("2. B2C Consumers")
        
        type_choice = Prompt.ask("Select type", choices=["1", "2"], default="1")
        persona_type = "b2b_saas" if type_choice == "1" else "b2c_consumer"
        
        return {
            "count": count,
            "persona_type": persona_type,
            "working_dir": str(self.working_dir),
            "experience_type": "just_do_it"
        }
    
    def _learning_config(self) -> dict:
        """Learning configuration with explanations"""
        console.print("[bold blue]🎓 Learning Mode Setup[/bold blue]")
        console.print("We'll walk through each option and explain why it matters.")
        console.print()
        
        # Count with explanation
        console.print("[bold]Number of personas:[/bold]")
        console.print("💡 [dim]Tip: 10-25 personas give good variety without overwhelming analysis[/dim]")
        count = IntPrompt.ask("Count", default=15, show_default=True)
        
        # Type with explanation
        console.print("\n[bold]Persona type:[/bold]")
        console.print("💡 [dim]This determines job titles, pain points, and goals[/dim]")
        console.print("1. B2B SaaS (Product Managers, CTOs, Growth leads)")
        console.print("2. B2C Consumer (Marketing Managers, Brand leads)")
        
        type_choice = Prompt.ask("Select type", choices=["1", "2"], default="1")
        persona_type = "b2b_saas" if type_choice == "1" else "b2c_consumer"
        
        # Working directory with explanation
        console.print("\n[bold]Output location:[/bold]")
        console.print("💡 [dim]Generate data where you need it - current project or specific folder[/dim]")
        current_dir = str(self.working_dir)
        console.print(f"Current directory: [cyan]{current_dir}[/cyan]")
        
        use_current = Confirm.ask("Use current directory?", default=True)
        working_dir = current_dir if use_current else Prompt.ask("Enter directory path")
        
        # Data fields with explanations
        console.print("\n[bold]Data fields to include:[/bold]")
        console.print("💡 [dim]Each field adds realism but increases file size[/dim]")
        
        include_demographics = Confirm.ask("Demographics (age, location, company size)?", default=True)
        include_psychographics = Confirm.ask("Psychographics (personality, decision style)?", default=True)
        include_pain_points = Confirm.ask("Pain points and challenges?", default=True)
        include_goals = Confirm.ask("Goals and objectives?", default=True)
        
        # Output format
        console.print("\n[bold]Output format:[/bold]")
        console.print("1. JSON (structured, good for analysis)")
        console.print("2. CSV (spreadsheet-friendly)")
        
        format_choice = Prompt.ask("Select format", choices=["1", "2"], default="1")
        output_format = "json" if format_choice == "1" else "csv"
        
        return {
            "count": count,
            "persona_type": persona_type,
            "working_dir": working_dir,
            "output_format": output_format,
            "include_demographics": include_demographics,
            "include_psychographics": include_psychographics,
            "include_pain_points": include_pain_points,
            "include_goals": include_goals,
            "experience_type": "learn_and_do"
        }
    
    def _advanced_config(self) -> dict:
        """Advanced configuration for CLI experts"""
        console.print("[bold red]🔧 Advanced CLI Configuration[/bold red]")
        console.print("Full control over data generation parameters.")
        console.print()
        
        # Show current working directory
        console.print(f"Current working directory: [cyan]{self.working_dir}[/cyan]")
        
        # All parameters with advanced options
        count = IntPrompt.ask("Personas to generate", default=20)
        
        # Advanced persona type selection
        console.print("\nPersona types:")
        console.print("1. B2B SaaS Professionals")
        console.print("2. B2C Consumer Market")
                
        type_choice = Prompt.ask("Persona type", choices=["1", "2"], default="1")
        persona_type = "b2b_saas" if type_choice == "1" else "b2c_consumer"
        
        # Working directory
        change_dir = Confirm.ask("Change working directory?", default=False)
        working_dir = str(self.working_dir)
        if change_dir:
            working_dir = Prompt.ask("Working directory", default=str(self.working_dir))
        
        # Advanced data options
        console.print("\n[bold]Data Configuration:[/bold]")
        include_demographics = Confirm.ask("Include demographics?", default=True)
        include_psychographics = Confirm.ask("Include psychographics?", default=True)
        include_pain_points = Confirm.ask("Include pain points?", default=True)
        include_goals = Confirm.ask("Include goals?", default=True)
        
        # Output format
        console.print("\nOutput formats:")
        console.print("1. JSON")
        console.print("2. CSV")
        
        format_choice = Prompt.ask("Output format", choices=["1", "2"], default="1")
        output_format = "json" if format_choice == "1" else "csv"
        
        return {
            "count": count,
            "persona_type": persona_type,
            "working_dir": working_dir,
            "output_format": output_format,
            "include_demographics": include_demographics,
            "include_psychographics": include_psychographics,
            "include_pain_points": include_pain_points,
            "include_goals": include_goals,
            "experience_type": "cli_deep_dive"
        }
    
    def generate_data(self, config: dict) -> dict:
        """Generate data with progress indicator"""
        console.print()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                f"Generating {config['count']} {config['persona_type']} personas...", 
                total=None
            )
            
            # Call the shared data generator
            result = generate_sample_data(
                experience_type=config['experience_type'],
                working_dir=config['working_dir'],
                count=config['count'],
                persona_type=config['persona_type']
            )
            
            progress.update(task, completed=True)
        
        return result
    
    def show_results(self, result: dict, experience_type: str):
        """Display generation results"""
        console.print()
        
        if result['success']:
            # Success panel
            success_panel = Panel(
                f"[green]✅ Generated {result['stats']['total_personas']} personas[/green]\n"
                f"[blue]📁 Saved to: {result['output_file']}[/blue]",
                title="🎉 Generation Complete",
                border_style="green"
            )
            console.print(success_panel)
            
            # Statistics table
            self._show_stats_table(result['stats'])
            
            # Sample persona
            if result.get('sample_persona'):
                self._show_sample_persona(result['sample_persona'])
            
            # Learning insights for learning mode
            if experience_type == "learn_and_do":
                self._show_learning_insights(result)
            
            # Command for CLI deep dive
            elif experience_type == "cli_deep_dive":
                self._show_cli_insights(result)
        
        else:
            error_panel = Panel(
                f"[red]❌ Generation failed[/red]\n{result.get('error', 'Unknown error')}",
                title="Error",
                border_style="red"
            )
            console.print(error_panel)
    
    def _show_stats_table(self, stats: dict):
        """Show statistics in a formatted table"""
        table = Table(title="📊 Generation Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Personas", str(stats['total_personas']))
        table.add_row("Unique Companies", str(stats['unique_companies']))
        
        if stats.get('average_age'):
            table.add_row("Average Age", f"{stats['average_age']} years")
        
        # Company size distribution
        if stats.get('company_size_distribution'):
            for size, count in stats['company_size_distribution'].items():
                table.add_row(f"Company Size {size}", str(count))
        
        console.print(table)
        console.print()
    
    def _show_sample_persona(self, persona: dict):
        """Show a sample persona"""
        sample_text = f"""[bold]👤 Sample Persona[/bold]

[cyan]Name:[/cyan] {persona['name']}
[cyan]Title:[/cyan] {persona['title']}
[cyan]Company:[/cyan] {persona['company']}
[cyan]Email:[/cyan] {persona['email']}

[yellow]Pain Points:[/yellow]
{chr(10).join('• ' + point for point in persona.get('pain_points', []))}

[green]Goals:[/green]
{chr(10).join('• ' + goal for goal in persona.get('goals', []))}
"""
        
        sample_panel = Panel(
            sample_text,
            title="Sample Data",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(sample_panel)
        console.print()
    
    def _show_learning_insights(self, result: dict):
        """Show learning insights for educational mode"""
        insights = """[bold yellow]🎓 What You Just Learned[/bold yellow]

[green]✓[/green] [bold]Data Structure:[/bold] Each persona contains demographics, psychographics, pain points, and goals
[green]✓[/green] [bold]Realistic Patterns:[/bold] Data follows real-world distributions (company sizes, age ranges)
[green]✓[/green] [bold]Product Validation:[/bold] Use this data to test assumptions before building features
[green]✓[/green] [bold]Research Foundation:[/bold] Synthetic data guides user interviews and surveys

[bold]Next Steps:[/bold]
• Analyze pain points to identify product opportunities
• Use goals to validate your product's value proposition
• Test your UI/UX with these realistic personas
• Generate more data for A/B testing scenarios
"""
        
        learning_panel = Panel(
            insights,
            title="Learning Insights",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(learning_panel)
    
    def _show_cli_insights(self, result: dict):
        """Show CLI mastery insights"""
        config = result['config']
        
        # Show equivalent command
        cmd_parts = [
            "python shared/data_generator.py",
            f"--count={config['count']}",
            f"--type={config['persona_type']}",
            f"--experience={config['experience_type']}",
            f"--dir=\"{config['working_dir']}\""
        ]
        
        command = " ".join(cmd_parts)
        
        insights = f"""[bold red]🔧 CLI Mastery[/bold red]

[bold]Equivalent Command:[/bold]
[blue]{command}[/blue]

[bold]Script This Generation:[/bold]
• Save the command above for automation
• Use it in bash scripts or CI/CD pipelines  
• Modify parameters for different scenarios
• Combine with other CLI tools for workflows

[bold]Advanced Options:[/bold]
• Add [cyan]--format=csv[/cyan] for spreadsheet output
• Use [cyan]--interactive[/cyan] for guided mode
• Chain with [cyan]| jq[/cyan] for JSON processing
"""
        
        cli_panel = Panel(
            insights,
            title="CLI Deep Dive",
            border_style="red",
            padding=(1, 2)
        )
        console.print(cli_panel)

def main(experience_type: Optional[str] = None):
    """Main CLI entry point"""
    cli_gen = CLIDataGenerator()
    
    try:
        console.clear()
        cli_gen.show_header()
        
        # Select experience if not provided
        if not experience_type:
            experience_type = cli_gen.select_experience()
        
        # Configure generation
        config = cli_gen.configure_generation(experience_type)
        
        # Generate data
        result = cli_gen.generate_data(config)
        
        # Show results
        cli_gen.show_results(result, experience_type)
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Generation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - Data Generation CLI")
    parser.add_argument("--experience", choices=["just_do_it", "learn_and_do", "cli_deep_dive"],
                       help="Experience type")
    
    args = parser.parse_args()
    main(args.experience)