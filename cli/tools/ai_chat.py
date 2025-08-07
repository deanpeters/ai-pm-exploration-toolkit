#!/usr/bin/env python3
"""
AI PM Toolkit - AI Chat CLI Tool
Local LLM integration for product manager assistance and brainstorming
"""

import sys
import os
import argparse
from pathlib import Path

# Add shared directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import box
    from rich.text import Text
    from rich.markdown import Markdown
except ImportError:
    print("❌ Rich library not found. Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import box
    from rich.text import Text
    from rich.markdown import Markdown

# Import from shared module with specific path to avoid naming conflict
shared_path = str(Path(__file__).parent.parent.parent / "shared")
if shared_path not in sys.path:
    sys.path.insert(0, shared_path)

# Import with module alias to avoid naming conflict
import importlib.util
spec = importlib.util.spec_from_file_location("ai_chat_shared", Path(__file__).parent.parent.parent / "shared" / "ai_chat.py")
ai_chat_shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai_chat_shared)

start_ai_chat = ai_chat_shared.start_ai_chat
AIChat = ai_chat_shared.AIChat  
ChatConfig = ai_chat_shared.ChatConfig

console = Console()

class CLIAIChat:
    """CLI interface for AI chat with rich output"""
    
    def __init__(self):
        self.chat_engine = None
        self.config = None
        self.working_dir = Path.cwd()
    
    def show_header(self):
        """Display the tool header"""
        title = Text("🤖 AI Product Management Assistant", style="bold blue")
        subtitle = Text("Chat with AI for product strategy, brainstorming, and analysis", style="dim")
        
        header_panel = Panel(
            Text.assemble(title, "\n", subtitle),
            box=box.DOUBLE,
            padding=(1, 2),
            style="blue"
        )
        
        console.print(header_panel)
        console.print()
    
    def select_chat_mode(self) -> str:
        """Let user select chat mode"""
        console.print("[bold]Choose your AI assistant mode:[/bold]")
        console.print()
        
        modes = {
            "1": ("pm_assistant", "🎯 PM Assistant", "Product strategy, roadmaps, and best practices"),
            "2": ("brainstorm", "💡 Creative Brainstorm", "Idea generation and creative problem solving"),
            "3": ("analysis", "📊 Data Analysis", "Market research interpretation and insights")
        }
        
        for key, (mode_id, name, desc) in modes.items():
            console.print(f"{key}. {name}")
            console.print(f"   {desc}")
            console.print()
        
        choice = Prompt.ask("Select chat mode", choices=list(modes.keys()), default="1")
        return modes[choice][0]
    
    def select_experience(self) -> str:
        """Let user select experience type"""
        console.print("[bold]Choose your learning experience:[/bold]")
        console.print()
        
        experiences = {
            "1": ("just_do_it", "🚀 Just Chat", "Quick AI responses, no frills"),
            "2": ("learn_and_do", "🎓 Learn & Chat", "Explanations and educational context"), 
            "3": ("cli_deep_dive", "🔧 Power User", "Advanced features and customization")
        }
        
        for key, (exp_id, name, desc) in experiences.items():
            console.print(f"{key}. {name}")
            console.print(f"   {desc}")
            console.print()
        
        choice = Prompt.ask("Select experience", choices=list(experiences.keys()), default="1")
        return experiences[choice][0]
    
    def setup_chat_session(self, chat_mode: str, experience_type: str) -> bool:
        """Setup the chat session"""
        try:
            console.print(f"\n[yellow]🤖 Initializing AI chat session...[/yellow]")
            
            result = start_ai_chat(
                chat_mode=chat_mode,
                model="local",
                experience_type=experience_type,
                working_dir=str(self.working_dir)
            )
            
            if result["success"]:
                self.chat_engine = result["chat_engine"]
                self.config = ChatConfig(**result["config"])
                
                # Show session info
                session_info = result["session_info"]
                info_panel = Panel(
                    f"[green]✅ Chat session started![/green]\n"
                    f"[blue]Session ID:[/blue] {session_info['session_id']}\n"
                    f"[blue]Mode:[/blue] {chat_mode}\n"
                    f"[blue]Model:[/blue] {session_info['model']}\n"
                    f"[blue]Available models:[/blue] {', '.join(session_info['available_models'].keys())}",
                    title="🤖 Session Info",
                    border_style="green"
                )
                console.print(info_panel)
                console.print()
                
                return True
            else:
                console.print("[red]❌ Failed to start chat session[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]❌ Error setting up chat: {e}[/red]")
            return False
    
    def show_chat_help(self, experience_type: str):
        """Show chat help and commands"""
        if experience_type == "just_do_it":
            help_text = """[bold]Chat Commands:[/bold]
• Type your questions or ideas naturally
• Type 'quit' or 'exit' to end the session
• Type 'help' to see this message again
"""
        elif experience_type == "learn_and_do":
            help_text = """[bold]Chat Commands & Learning Tips:[/bold]
• Type your questions or ideas naturally
• Ask for explanations: "Explain why this approach works"
• Request examples: "Give me an example of this in practice"
• Type 'quit' or 'exit' to end the session
• Type 'save' to save conversation history
• Type 'help' to see this message again

[bold]Learning Mode Features:[/bold]
• AI provides detailed explanations and context
• Responses include practical examples and frameworks
• Conversation history is automatically saved
"""
        else:  # cli_deep_dive
            help_text = """[bold]Advanced Chat Commands:[/bold]
• Type your questions or ideas naturally
• Type 'quit' or 'exit' to end the session
• Type 'save [filename]' to save conversation
• Type 'load [filename]' to load previous conversation
• Type 'summary' to get conversation summary
• Type 'help' to see this message again

[bold]Power User Features:[/bold]
• Conversation persistence and loading
• Session management and history
• Advanced AI model switching (if available)
• Export conversations in multiple formats
"""
        
        help_panel = Panel(
            help_text,
            title="💬 Chat Help",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(help_panel)
        console.print()
    
    def start_interactive_chat(self, experience_type: str):
        """Start interactive chat session"""
        self.show_chat_help(experience_type)
        
        console.print("[bold green]🚀 Chat session started! Ask me anything about product management.[/bold green]")
        console.print("[dim]Type 'help' for commands, 'quit' to exit[/dim]")
        console.print("=" * 60)
        console.print()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[bold cyan]You[/bold cyan]", default="").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    self.show_chat_help(experience_type)
                    continue
                elif user_input.lower().startswith('save'):
                    self.handle_save_command(user_input, experience_type)
                    continue
                elif user_input.lower().startswith('load') and experience_type == "cli_deep_dive":
                    self.handle_load_command(user_input)
                    continue
                elif user_input.lower() == 'summary' and experience_type == "cli_deep_dive":
                    self.show_conversation_summary()
                    continue
                
                # Send message to AI
                console.print()
                with console.status("[yellow]🤖 AI is thinking...[/yellow]"):
                    response = self.chat_engine.send_message(user_input, self.config)
                
                # Display AI response
                ai_text = Text("AI Assistant: ", style="bold magenta")
                console.print(ai_text, end="")
                console.print(response["response"])
                
                if experience_type in ["learn_and_do", "cli_deep_dive"]:
                    console.print(f"[dim]Tokens: {response['tokens_used']} | Messages: {response['conversation_length']}[/dim]")
                
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Chat interrupted[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        # Save conversation on exit if appropriate
        if self.config.save_conversation and experience_type != "just_do_it":
            filename = self.chat_engine.save_conversation()
            console.print(f"[green]💾 Conversation saved to: {filename}[/green]")
    
    def handle_save_command(self, command: str, experience_type: str):
        """Handle save command"""
        parts = command.split()
        filename = parts[1] if len(parts) > 1 else None
        
        try:
            saved_file = self.chat_engine.save_conversation(filename)
            console.print(f"[green]💾 Conversation saved to: {saved_file}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Save failed: {e}[/red]")
    
    def handle_load_command(self, command: str):
        """Handle load command"""
        parts = command.split()
        if len(parts) < 2:
            console.print("[red]Usage: load <filename>[/red]")
            return
        
        filename = parts[1]
        try:
            if self.chat_engine.load_conversation(filename):
                console.print(f"[green]📂 Conversation loaded from: {filename}[/green]")
            else:
                console.print(f"[red]❌ Failed to load: {filename}[/red]")
        except Exception as e:
            console.print(f"[red]❌ Load failed: {e}[/red]")
    
    def show_conversation_summary(self):
        """Show conversation summary"""
        try:
            summary = self.chat_engine.get_conversation_summary()
            
            summary_table = Table(title="📊 Conversation Summary", box=box.ROUNDED)
            summary_table.add_column("Metric", style="cyan")
            summary_table.add_column("Value", style="white")
            
            summary_table.add_row("Total Messages", str(summary["message_count"]))
            summary_table.add_row("Your Messages", str(summary["user_messages"]))
            summary_table.add_row("AI Responses", str(summary["assistant_messages"]))
            summary_table.add_row("Total Tokens", str(summary["total_tokens"]))
            
            if summary["conversation_start"]:
                summary_table.add_row("Started", summary["conversation_start"])
            if summary["last_message"]:    
                summary_table.add_row("Last Message", summary["last_message"])
            
            console.print(summary_table)
            console.print()
            
        except Exception as e:
            console.print(f"[red]❌ Error getting summary: {e}[/red]")
    
    def run_demo_chat(self, chat_mode: str):
        """Run demo chat session"""
        console.print("[bold]🎬 Demo Chat Session[/bold]")
        console.print("Demonstrating AI chat capabilities with sample questions...")
        console.print()
        
        demo_questions = {
            "pm_assistant": [
                "How should I prioritize features in my product roadmap?",
                "What metrics should I track for user engagement?",
                "How do I validate a new product idea with users?"
            ],
            "brainstorm": [
                "Help me brainstorm innovative features for a task management app",
                "What are creative ways to improve user onboarding?",
                "Generate ideas for making our product more social"
            ],
            "analysis": [
                "How should I interpret declining user retention rates?",
                "What does increasing time-to-value mean for our product?",
                "Analyze the competitive landscape for our market segment"
            ]
        }
        
        questions = demo_questions.get(chat_mode, demo_questions["pm_assistant"])
        
        for i, question in enumerate(questions, 1):
            console.print(f"[bold cyan]Demo Question {i}:[/bold cyan] {question}")
            
            with console.status("[yellow]🤖 AI is thinking...[/yellow]"):
                response = self.chat_engine.send_message(question, self.config)
            
            console.print(f"[bold magenta]AI Response:[/bold magenta] {response['response']}")
            console.print(f"[dim]Tokens: {response['tokens_used']}[/dim]")
            console.print("-" * 60)
            console.print()
        
        console.print("[green]🎬 Demo completed![/green]")

def main(experience_type=None, chat_mode=None, demo=False):
    """Main CLI entry point"""
    cli_chat = CLIAIChat()
    
    try:
        console.clear()
        cli_chat.show_header()
        
        # Select chat mode if not provided
        if not chat_mode:
            chat_mode = cli_chat.select_chat_mode()
        
        # Select experience if not provided  
        if not experience_type:
            experience_type = cli_chat.select_experience()
        
        # Setup chat session
        if not cli_chat.setup_chat_session(chat_mode, experience_type):
            return
        
        # Run appropriate chat mode
        if demo:
            cli_chat.run_demo_chat(chat_mode)
        else:
            cli_chat.start_interactive_chat(experience_type)
        
        console.print("\n[green]👋 Thanks for chatting! Your AI assistant is always here to help.[/green]")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Chat session cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI PM Toolkit - AI Chat CLI")
    parser.add_argument("--experience", choices=["just_do_it", "learn_and_do", "cli_deep_dive"],
                       help="Experience type")
    parser.add_argument("--mode", choices=["pm_assistant", "brainstorm", "analysis"],
                       help="Chat mode")
    parser.add_argument("--demo", action="store_true", help="Run demo chat session")
    
    args = parser.parse_args()
    main(args.experience, args.mode, args.demo)