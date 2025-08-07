#!/usr/bin/env python3
"""
AI PM Toolkit - CLI Dashboard
Phase 1: Beautiful terminal interface with rich library
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
except ImportError:
    print("❌ Rich library not found. Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    from rich import box

# Initialize console
console = Console()

# Load toolkit configuration
TOOLKIT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = TOOLKIT_ROOT / "toolkit.json"

def load_config() -> Dict:
    """Load toolkit configuration"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/red]")
        return {"tools": [], "experiences": {}}

def show_header():
    """Display the main header"""
    title = Text("🧪 AI PM Toolkit - CLI Dashboard", style="bold cyan")
    subtitle = Text("Proof-of-Life Probes for Product Managers", style="dim")
    
    header_panel = Panel(
        Text.assemble(title, "\n", subtitle),
        box=box.DOUBLE,
        padding=(1, 2),
        style="cyan"
    )
    
    console.print(header_panel)
    console.print()

def show_tools_table(config: Dict):
    """Display tools in a formatted table"""
    tools = config.get('tools', [])
    
    table = Table(title="Available Tools", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Status", justify="center")
    table.add_column("Description", style="dim")
    
    for i, tool in enumerate(tools, 1):
        status_style = {
            'working': '[green]✅ Working[/green]',
            'planned': '[yellow]🚧 Planned[/yellow]',
            'disabled': '[red]❌ Disabled[/red]'
        }.get(tool.get('status', 'unknown'), '[dim]❓ Unknown[/dim]')
        
        table.add_row(
            str(i),
            tool.get('name', 'Unknown'),
            status_style,
            tool.get('description', 'No description')[:50] + "..." if len(tool.get('description', '')) > 50 else tool.get('description', '')
        )
    
    console.print(table)
    console.print()

def show_experiences(config: Dict):
    """Display available experience types"""
    experiences = config.get('experiences', {})
    
    console.print("[bold]Choose Your Learning Experience:[/bold]")
    console.print()
    
    for exp_id, exp_data in experiences.items():
        icon = {
            'just_do_it': '🚀',
            'learn_and_do': '🎓', 
            'cli_deep_dive': '🔧'
        }.get(exp_id, '📋')
        
        panel = Panel(
            f"[bold]{exp_data.get('name', exp_id)}[/bold]\n{exp_data.get('description', 'No description')}",
            title=f"{icon} {exp_id.replace('_', ' ').title()}",
            border_style="blue",
            padding=(0, 1)
        )
        console.print(panel)
    
    console.print()

def select_tool(config: Dict) -> Optional[Dict]:
    """Let user select a tool"""
    tools = config.get('tools', [])
    
    if not tools:
        console.print("[red]No tools available![/red]")
        return None
    
    console.print("[bold cyan]Select a tool:[/bold cyan]")
    
    choices = []
    for i, tool in enumerate(tools, 1):
        status_emoji = {
            'working': '✅',
            'planned': '🚧',
            'disabled': '❌'
        }.get(tool.get('status', 'unknown'), '❓')
        
        choice_text = f"{i}. {status_emoji} {tool.get('name', 'Unknown')}"
        choices.append(str(i))
        console.print(choice_text)
    
    choices.extend(['q', 'quit', 'exit', 'web'])
    console.print("w. 🌐 Switch to Web Dashboard")
    console.print("q. 🚪 Quit")
    console.print()
    
    choice = Prompt.ask("Enter your choice", choices=choices, default="q")
    
    if choice.lower() in ['q', 'quit', 'exit']:
        return None
    elif choice.lower() in ['w', 'web']:
        return {'action': 'web'}
    
    try:
        tool_index = int(choice) - 1
        if 0 <= tool_index < len(tools):
            return tools[tool_index]
    except ValueError:
        pass
    
    console.print("[red]Invalid choice![/red]")
    return None

def select_experience(tool: Dict, config: Dict) -> Optional[str]:
    """Let user select an experience type"""
    tool_experiences = tool.get('experiences', [])
    experiences = config.get('experiences', {})
    
    console.print(f"\n[bold]Select experience for {tool.get('name')}:[/bold]")
    
    choices = []
    for i, exp_id in enumerate(tool_experiences, 1):
        exp_data = experiences.get(exp_id, {})
        icon = {
            'just_do_it': '🚀',
            'learn_and_do': '🎓',
            'cli_deep_dive': '🔧'
        }.get(exp_id, '📋')
        
        choice_text = f"{i}. {icon} {exp_data.get('name', exp_id)}"
        choices.append(str(i))
        console.print(choice_text)
    
    choices.extend(['b', 'back'])
    console.print("b. ← Back to tool selection")
    console.print()
    
    choice = Prompt.ask("Enter your choice", choices=choices, default="b")
    
    if choice.lower() in ['b', 'back']:
        return None
    
    try:
        exp_index = int(choice) - 1
        if 0 <= exp_index < len(tool_experiences):
            return tool_experiences[exp_index]
    except ValueError:
        pass
    
    console.print("[red]Invalid choice![/red]")
    return None

def launch_tool(tool: Dict, experience: str):
    """Launch a tool with specified experience"""
    console.print()
    
    tool_id = tool.get('id', 'unknown')
    
    # Handle different tools
    if tool_id == 'data-generation':
        launch_data_generation_tool(experience)
    elif tool_id == 'market-research':
        launch_market_research_tool(experience)
    elif tool_id == 'ai-chat':
        launch_ai_chat_tool(experience)
    elif tool_id == 'n8n-workflows':
        launch_n8n_workflows()
    else:
        # Generic placeholder for other tools
        show_tool_placeholder(tool, experience)

def launch_data_generation_tool(experience: str):
    """Launch the data generation CLI tool"""
    try:
        # Import and run the data generation CLI
        import subprocess
        import sys
        
        # Path to the CLI tool
        script_path = Path(__file__).parent / "tools" / "data_gen.py"
        
        # Run the tool with the specified experience
        cmd = [sys.executable, str(script_path)]
        if experience:
            cmd.extend(["--experience", experience])
        
        # Run the tool
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            console.print("[green]✅ Data generation completed successfully![/green]")
        else:
            console.print("[red]❌ Data generation encountered an error[/red]")
            
    except Exception as e:
        console.print(f"[red]Error launching data generation tool: {e}[/red]")
        console.print("[yellow]Falling back to direct import...[/yellow]")
        
        try:
            # Fallback: import and run directly
            sys.path.append(str(Path(__file__).parent / "tools"))
            from data_gen import main as data_gen_main
            data_gen_main(experience)
        except Exception as e2:
            console.print(f"[red]Fallback also failed: {e2}[/red]")

def launch_market_research_tool(experience: str):
    """Launch the market research CLI tool"""
    try:
        # Import and run the market research CLI
        import subprocess
        import sys
        
        # Path to the CLI tool
        script_path = Path(__file__).parent / "tools" / "market_research.py"
        
        # Run the tool with the specified experience
        cmd = [sys.executable, str(script_path)]
        if experience:
            cmd.extend(["--experience", experience])
        
        # Run the tool
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            console.print("[green]✅ Market research completed successfully![/green]")
        else:
            console.print("[red]❌ Market research encountered an error[/red]")
            
    except Exception as e:
        console.print(f"[red]Error launching market research tool: {e}[/red]")
        console.print("[yellow]Falling back to direct import...[/yellow]")
        
        try:
            # Fallback: import and run directly
            sys.path.append(str(Path(__file__).parent / "tools"))
            from market_research import main as market_research_main
            market_research_main(experience)
        except Exception as e2:
            console.print(f"[red]Fallback also failed: {e2}[/red]")

def launch_ai_chat_tool(experience: str):
    """Launch the AI chat CLI tool"""
    try:
        # Import and run the AI chat CLI
        import subprocess
        import sys
        
        # Path to the CLI tool
        script_path = Path(__file__).parent / "tools" / "ai_chat.py"
        
        # Run the tool with the specified experience
        cmd = [sys.executable, str(script_path)]
        if experience:
            cmd.extend(["--experience", experience])
        
        # Run the tool
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            console.print("[green]✅ AI chat session completed successfully![/green]")
        else:
            console.print("[red]❌ AI chat session encountered an error[/red]")
            
    except Exception as e:
        console.print(f"[red]Error launching AI chat tool: {e}[/red]")
        console.print("[yellow]Falling back to direct import...[/yellow]")
        
        try:
            # Fallback: import and run directly
            sys.path.append(str(Path(__file__).parent / "tools"))
            from ai_chat import main as ai_chat_main
            ai_chat_main(experience)
        except Exception as e2:
            console.print(f"[red]Fallback also failed: {e2}[/red]")

def launch_n8n_workflows():
    """Launch n8n workflows (existing functionality)"""
    console.print()
    
    panel_content = """[bold green]🔧 n8n Workflow Automation[/bold green]

[bold]Status:[/bold] Working from Phase 1!

This will launch the existing n8n workflow orchestration system.

[dim]Command to execute:[/dim]
[cyan]cd workflow-tools && ./orchestrate-workflows.sh start[/cyan]

[bold]Available at:[/bold] http://localhost:5678 (after startup)
"""
    
    panel = Panel(
        panel_content,
        title="n8n Workflows",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    if Confirm.ask("Launch n8n workflows?", default=True):
        try:
            import subprocess
            script_path = Path(__file__).parent.parent / "workflow-tools" / "orchestrate-workflows.sh"
            subprocess.run([str(script_path), "start"])
        except Exception as e:
            console.print(f"[red]Error launching n8n: {e}[/red]")
    
    input("Press Enter to continue...")

def show_tool_placeholder(tool: Dict, experience: str):
    """Show placeholder for tools not yet implemented"""
    panel_content = f"""[bold yellow]🚧 Tool Coming Soon[/bold yellow]

[bold]Tool:[/bold] {tool.get('name', 'Unknown')}
[bold]Experience:[/bold] {experience}
[bold]Status:[/bold] {tool.get('status', 'unknown')}

[yellow]This tool will be implemented in Phase 3.[/yellow]

[dim]Planned command:[/dim]
[cyan]python cli/tools/{tool.get('id', 'unknown').replace('-', '_')}.py --experience={experience}[/cyan]

[bold]What you can do now:[/bold]
• Try the data generation tool (working in Phase 2)
• Use n8n workflows (working from Phase 1)
• Check the web interface for more options
"""
    
    panel = Panel(
        panel_content,
        title="🛠️ Tool Placeholder",
        border_style="yellow",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    input("Press Enter to continue...")

def switch_to_web():
    """Instructions for switching to web interface"""
    console.print()
    
    panel_content = """[bold cyan]🌐 Switching to Web Dashboard[/bold cyan]

To access the web interface, run this command in another terminal:

[bold green]aipm hub[/bold green]

Or start it manually:

[bold green]cd ~/aipm-toolkit/web && python app.py[/bold green]

Then open: [link]http://localhost:3000[/link]

[dim]The web interface will be available while this CLI dashboard continues running.[/dim]
"""
    
    panel = Panel(
        panel_content,
        title="🔄 Interface Switch",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)
    input("\nPress Enter to continue...")

def show_system_status(config: Dict):
    """Show system status and configuration"""
    console.print()
    
    status_content = f"""[bold green]System Status[/bold green]

[bold]Version:[/bold] {config.get('version', '1.0.0')}
[bold]Tools Available:[/bold] {len(config.get('tools', []))}
[bold]Experiences:[/bold] {len(config.get('experiences', {}))}
[bold]Config File:[/bold] {CONFIG_PATH}

[bold]Interfaces:[/bold]
• CLI Dashboard: ✅ Running
• Web Dashboard: Use 'aipm hub' to start

[bold]Phase 1 Status:[/bold]
• ✅ Core configuration system
• ✅ Web dashboard interface  
• ✅ CLI dashboard interface
• 🚧 Tool implementations (Phase 2)
"""
    
    panel = Panel(
        status_content,
        title="📊 System Status",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    input("\nPress Enter to continue...")

def main():
    """Main CLI dashboard loop"""
    config = load_config()
    
    console.clear()
    
    try:
        while True:
            console.clear()
            show_header()
            show_tools_table(config)
            show_experiences(config)
            
            # Add system options
            console.print("[bold]System Options:[/bold]")
            console.print("s. 📊 System Status")
            console.print("w. 🌐 Switch to Web Dashboard") 
            console.print("q. 🚪 Quit")
            console.print()
            
            # Get user choice
            choice = Prompt.ask(
                "What would you like to do?",
                choices=['s', 'status', 'w', 'web', 'q', 'quit'] + [str(i) for i in range(1, len(config.get('tools', [])) + 1)],
                default="q"
            )
            
            if choice.lower() in ['q', 'quit']:
                console.print("\n[green]👋 Thanks for using AI PM Toolkit![/green]")
                break
            elif choice.lower() in ['s', 'status']:
                show_system_status(config)
            elif choice.lower() in ['w', 'web']:
                switch_to_web()
            else:
                # Tool selection
                try:
                    tool_index = int(choice) - 1
                    tools = config.get('tools', [])
                    if 0 <= tool_index < len(tools):
                        selected_tool = tools[tool_index]
                        
                        # Check if tool is working
                        if selected_tool.get('status') != 'working':
                            console.print(f"\n[yellow]⚠️ Tool '{selected_tool.get('name')}' is not yet available.[/yellow]")
                            console.print(f"[dim]Status: {selected_tool.get('status', 'unknown')}[/dim]")
                            console.print("[dim]This will be implemented in Phase 2.[/dim]")
                            input("\nPress Enter to continue...")
                            continue
                        
                        # Select experience
                        experience = select_experience(selected_tool, config)
                        if experience:
                            launch_tool(selected_tool, experience)
                except ValueError:
                    console.print("[red]Invalid choice![/red]")
                    input("Press Enter to continue...")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
    finally:
        console.print("[dim]Goodbye![/dim]")

if __name__ == "__main__":
    main()