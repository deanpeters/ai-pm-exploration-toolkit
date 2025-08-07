#!/usr/bin/env python3
"""
AI PM Toolkit - CLI Market Research Tool
Beautiful command-line interface for market research and competitive intelligence
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

# Import from shared module with specific path to avoid naming conflict
import importlib.util
spec = importlib.util.spec_from_file_location("market_research_shared", Path(__file__).parent.parent.parent / "shared" / "market_research.py")
market_research_shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(market_research_shared)

research_company_data = market_research_shared.research_company_data
research_market_data = market_research_shared.research_market_data
MarketResearcher = market_research_shared.MarketResearcher

console = Console()

class CLIMarketResearcher:
    """CLI interface for market research with rich output"""
    
    def __init__(self):
        self.researcher = MarketResearcher()
        self.working_dir = Path.cwd()
    
    def show_header(self):
        """Display the tool header"""
        title = Text("📊 Market Research & Competitive Intelligence", style="bold green")
        subtitle = Text("Research companies, markets, and competitive landscapes", style="dim")
        
        header_panel = Panel(
            Text.assemble(title, "\n", subtitle),
            box=box.DOUBLE,
            padding=(1, 2),
            style="green"
        )
        
        console.print(header_panel)
        console.print()
    
    def select_research_type(self) -> str:
        """Let user select research type"""
        console.print("[bold]Choose your research focus:[/bold]")
        console.print()
        
        research_types = {
            "1": ("company", "🏢 Company Research", "Analyze specific companies and competitors"),
            "2": ("market", "📈 Market Analysis", "Research market trends and opportunities")
        }
        
        for key, (research_id, name, desc) in research_types.items():
            console.print(f"{key}. {name}")
            console.print(f"   {desc}")
            console.print()
        
        choice = Prompt.ask("Select research type", choices=list(research_types.keys()), default="1")
        return research_types[choice][0]
    
    def select_experience(self) -> str:
        """Let user select experience type"""
        console.print("[bold]Choose your learning experience:[/bold]")
        console.print()
        
        experiences = {
            "1": ("just_do_it", "🚀 Just Do It", "Quick research with key insights"),
            "2": ("learn_and_do", "🎓 Learn & Do", "Detailed analysis with explanations"), 
            "3": ("cli_deep_dive", "🔧 CLI Deep Dive", "Advanced research with custom options")
        }
        
        for key, (exp_id, name, desc) in experiences.items():
            console.print(f"{key}. {name}")
            console.print(f"   {desc}")
            console.print()
        
        choice = Prompt.ask("Select experience", choices=list(experiences.keys()), default="1")
        return experiences[choice][0]
    
    def configure_company_research(self, experience_type: str) -> dict:
        """Configure company research parameters"""
        config = {}
        
        if experience_type == "just_do_it":
            config = self._quick_company_config()
        elif experience_type == "learn_and_do":
            config = self._learning_company_config()
        else:  # cli_deep_dive
            config = self._advanced_company_config()
        
        return config
    
    def configure_market_research(self, experience_type: str) -> dict:
        """Configure market research parameters"""
        config = {}
        
        if experience_type == "just_do_it":
            config = self._quick_market_config()
        elif experience_type == "learn_and_do":
            config = self._learning_market_config()
        else:  # cli_deep_dive
            config = self._advanced_market_config()
        
        return config
    
    def _quick_company_config(self) -> dict:
        """Quick company research configuration"""
        console.print("[bold blue]🚀 Quick Company Research[/bold blue]")
        
        # Company identification
        console.print("\nIdentify the company:")
        company_name = Prompt.ask("Company name", default="")
        ticker = Prompt.ask("Stock ticker (optional)", default="").upper()
        
        if not company_name and not ticker:
            console.print("[red]Please provide either company name or ticker[/red]")
            return self._quick_company_config()
        
        return {
            "research_type": "company",
            "company_name": company_name if company_name else None,
            "ticker": ticker if ticker else None,
            "working_dir": str(self.working_dir),
            "experience_type": "just_do_it"
        }
    
    def _learning_company_config(self) -> dict:
        """Learning company research configuration"""
        console.print("[bold blue]🎓 Company Research Learning Mode[/bold blue]")
        console.print("We'll guide you through comprehensive company analysis.")
        console.print()
        
        # Company identification with guidance
        console.print("[bold]Company Identification:[/bold]")
        console.print("💡 [dim]Tip: Public companies have stock tickers (AAPL, MSFT, GOOGL)[/dim]")
        company_name = Prompt.ask("Company name")
        ticker = Prompt.ask("Stock ticker (helps with financial data)", default="").upper() 
        
        # Research scope with explanations
        console.print("\n[bold]Research Scope:[/bold]")
        console.print("💡 [dim]Each component provides different strategic insights[/dim]")
        
        include_financials = Confirm.ask("Include financial analysis?", default=True)
        if include_financials:
            console.print("   [dim]→ Revenue, profitability, market cap, growth trends[/dim]")
        
        include_news = Confirm.ask("Include recent news & developments?", default=True)
        if include_news:
            console.print("   [dim]→ Product launches, partnerships, market moves[/dim]")
        
        include_competitors = Confirm.ask("Include competitive analysis?", default=True)
        if include_competitors:
            console.print("   [dim]→ Direct competitors, market positioning, SWOT[/dim]")
        
        # Working directory
        console.print("\n[bold]Output Configuration:[/bold]")
        console.print(f"Current directory: [cyan]{self.working_dir}[/cyan]")
        use_current = Confirm.ask("Save research here?", default=True)
        working_dir = str(self.working_dir) if use_current else Prompt.ask("Output directory")
        
        return {
            "research_type": "company",
            "company_name": company_name,
            "ticker": ticker if ticker else None,
            "include_financials": include_financials,
            "include_news": include_news,
            "include_competitors": include_competitors,
            "working_dir": working_dir,
            "experience_type": "learn_and_do"
        }
    
    def _advanced_company_config(self) -> dict:
        """Advanced company research configuration"""
        console.print("[bold red]🔧 Advanced Company Research[/bold red]")
        console.print("Full control over research parameters and data sources.")
        console.print()
        
        # Company identification
        company_name = Prompt.ask("Company name")
        ticker = Prompt.ask("Stock ticker", default="").upper()
        
        # Research depth
        console.print("\nResearch depth:")
        console.print("1. Basic (company info + key metrics)")
        console.print("2. Detailed (+ financials + news + competitors)")
        console.print("3. Comprehensive (+ analysis + recommendations)")
        
        depth_choice = Prompt.ask("Research depth", choices=["1", "2", "3"], default="2")
        depth_map = {"1": "basic", "2": "detailed", "3": "comprehensive"}
        research_depth = depth_map[depth_choice]
        
        # Advanced options
        include_financials = Confirm.ask("Include financial data?", default=True)
        include_news = Confirm.ask("Include news analysis?", default=True)
        include_competitors = Confirm.ask("Include competitive intelligence?", default=True)
        
        # Output options
        console.print("\nOutput format:")
        console.print("1. JSON (structured data)")
        console.print("2. CSV (spreadsheet format)")
        
        format_choice = Prompt.ask("Output format", choices=["1", "2"], default="1")
        output_format = "json" if format_choice == "1" else "csv"
        
        # Working directory
        change_dir = Confirm.ask("Change working directory?", default=False)
        working_dir = str(self.working_dir)
        if change_dir:
            working_dir = Prompt.ask("Working directory", default=str(self.working_dir))
        
        return {
            "research_type": "company",
            "company_name": company_name,
            "ticker": ticker if ticker else None,
            "research_depth": research_depth,
            "include_financials": include_financials,
            "include_news": include_news,
            "include_competitors": include_competitors,
            "output_format": output_format,
            "working_dir": working_dir,
            "experience_type": "cli_deep_dive"
        }
    
    def _quick_market_config(self) -> dict:
        """Quick market research configuration"""
        console.print("[bold green]🚀 Quick Market Research[/bold green]")
        
        # Market type selection
        console.print("\nWhat type of market are you researching?")
        console.print("1. B2B SaaS (Business software)")
        console.print("2. B2C Consumer (Consumer products)")
        console.print("3. FinTech (Financial technology)")
        
        market_choice = Prompt.ask("Market type", choices=["1", "2", "3"], default="1")
        market_map = {"1": "b2b_saas", "2": "b2c_consumer", "3": "fintech"}
        market_type = market_map[market_choice]
        
        # Industry
        industry = Prompt.ask("Industry focus", default="technology")
        
        return {
            "research_type": "market",
            "market_type": market_type,
            "industry": industry,
            "working_dir": str(self.working_dir),
            "experience_type": "just_do_it"
        }
    
    def _learning_market_config(self) -> dict:
        """Learning market research configuration"""
        console.print("[bold green]🎓 Market Research Learning Mode[/bold green]")
        console.print("We'll explore market dynamics and competitive landscapes together.")
        console.print()
        
        # Market definition with guidance
        console.print("[bold]Market Definition:[/bold]")
        console.print("💡 [dim]Choose the market that best matches your product or interest[/dim]")
        
        console.print("\n1. B2B SaaS - Business software and platforms")
        console.print("2. B2C Consumer - Direct-to-consumer products and services")
        console.print("3. FinTech - Financial technology and services")
        
        market_choice = Prompt.ask("Market type", choices=["1", "2", "3"], default="1")
        market_map = {"1": "b2b_saas", "2": "b2c_consumer", "3": "fintech"}
        market_type = market_map[market_choice]
        
        # Industry focus
        console.print("\n[bold]Industry Focus:[/bold]")
        console.print("💡 [dim]More specific = more actionable insights[/dim]")
        industry = Prompt.ask("Industry or vertical", default="technology")
        
        # Research scope
        console.print("\n[bold]Research Scope:[/bold]")
        console.print("1. Trends - Current market movements and directions")
        console.print("2. Competitors - Key players and competitive landscape")
        console.print("3. Sizing - Market size and growth projections") 
        console.print("4. Full Analysis - Comprehensive market intelligence")
        
        scope_choice = Prompt.ask("Research scope", choices=["1", "2", "3", "4"], default="4")
        scope_map = {"1": "trends", "2": "competitors", "3": "sizing", "4": "analysis"}
        research_scope = scope_map[scope_choice]
        
        # Time period
        console.print("\n[bold]Time Perspective:[/bold]")
        console.print("1. Recent (last 6 months)")
        console.print("2. Historical (2+ years)")
        console.print("3. Forecast (next 12 months)")
        
        time_choice = Prompt.ask("Time period", choices=["1", "2", "3"], default="1")
        time_map = {"1": "recent", "2": "historical", "3": "forecast"}
        time_period = time_map[time_choice]
        
        return {
            "research_type": "market",
            "market_type": market_type,
            "industry": industry,
            "research_scope": research_scope,
            "time_period": time_period,
            "working_dir": str(self.working_dir),
            "experience_type": "learn_and_do"
        }
    
    def _advanced_market_config(self) -> dict:
        """Advanced market research configuration"""
        console.print("[bold green]🔧 Advanced Market Research[/bold green]")
        console.print("Comprehensive market intelligence with custom parameters.")
        console.print()
        
        # Market parameters
        market_types = ["b2b_saas", "b2c_consumer", "fintech"]
        market_type = Prompt.ask("Market type", choices=market_types, default="b2b_saas")
        industry = Prompt.ask("Industry", default="technology")
        
        # Research configuration
        scopes = ["trends", "competitors", "sizing", "analysis"]
        research_scope = Prompt.ask("Research scope", choices=scopes, default="analysis")
        
        time_periods = ["recent", "historical", "forecast"]
        time_period = Prompt.ask("Time period", choices=time_periods, default="recent")
        
        # Output configuration
        formats = ["json", "csv"]
        output_format = Prompt.ask("Output format", choices=formats, default="json")
        
        # Working directory
        change_dir = Confirm.ask("Change working directory?", default=False)
        working_dir = str(self.working_dir)
        if change_dir:
            working_dir = Prompt.ask("Working directory", default=str(self.working_dir))
        
        return {
            "research_type": "market",
            "market_type": market_type,
            "industry": industry,
            "research_scope": research_scope,
            "time_period": time_period,
            "output_format": output_format,
            "working_dir": working_dir,
            "experience_type": "cli_deep_dive"
        }
    
    def conduct_research(self, config: dict) -> dict:
        """Conduct research with progress indicator"""
        console.print()
        
        research_type = config["research_type"]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            if research_type == "company":
                task = progress.add_task(
                    f"Researching {config.get('company_name') or config.get('ticker')}...", 
                    total=None
                )
                
                result = research_company_data(
                    ticker=config.get("ticker"),
                    company_name=config.get("company_name"),
                    experience_type=config["experience_type"],
                    working_dir=config["working_dir"]
                )
            else:
                task = progress.add_task(
                    f"Analyzing {config['market_type']} market in {config['industry']}...", 
                    total=None
                )
                
                result = research_market_data(
                    industry=config["industry"],
                    market_type=config["market_type"],
                    experience_type=config["experience_type"],
                    working_dir=config["working_dir"]
                )
            
            progress.update(task, completed=True)
        
        return result
    
    def show_results(self, result: dict, experience_type: str):
        """Display research results"""
        console.print()
        
        if result['success']:
            # Success panel
            success_panel = Panel(
                f"[green]✅ Research completed successfully![/green]\n"
                f"[blue]📁 Saved to: {result['output_file']}[/blue]",
                title="🎉 Research Complete",
                border_style="green"
            )
            console.print(success_panel)
            
            # Show research summary
            if "company_info" in result["results"]:
                self._show_company_results(result["results"])
            elif "market_overview" in result["results"]:
                self._show_market_results(result["results"])
            
            # Learning insights for learning mode
            if experience_type == "learn_and_do":
                self._show_learning_insights(result)
            
            # CLI insights for deep dive
            elif experience_type == "cli_deep_dive":
                self._show_cli_insights(result)
        
        else:
            error_panel = Panel(
                f"[red]❌ Research failed[/red]\n{result.get('error', 'Unknown error')}",
                title="Error",
                border_style="red"
            )
            console.print(error_panel)
    
    def _show_company_results(self, results: dict):
        """Show company research results"""
        company_info = results["company_info"]
        
        # Company overview table
        table = Table(title=f"🏢 {company_info['name']} Overview", box=box.ROUNDED)
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Sector", company_info["sector"])
        table.add_row("Founded", company_info["founded"])
        table.add_row("Employees", company_info["employees"])
        table.add_row("Headquarters", company_info["headquarters"])
        
        console.print(table)
        console.print()
        
        # Competitors
        if results.get("competitors"):
            console.print("[bold]🥊 Key Competitors:[/bold]")
            for competitor in results["competitors"][:3]:
                console.print(f"  • {competitor['name']} ({competitor['relationship']} competitor)")
            console.print()
        
        # News highlights
        if results.get("news"):
            console.print("[bold]📰 Recent Developments:[/bold]")
            for news in results["news"][:2]:
                console.print(f"  • {news['title']}")
            console.print()
    
    def _show_market_results(self, results: dict):
        """Show market research results"""
        market_overview = results["market_overview"]
        
        # Market overview
        console.print(f"[bold green]📈 {market_overview['market_type'].upper()} Market Analysis[/bold green]")
        console.print(f"Industry: {market_overview['industry']}")
        console.print(f"Maturity: {market_overview['maturity']}")
        console.print()
        
        # Top trends
        if results.get("trends"):
            console.print("[bold]🔥 Key Market Trends:[/bold]")
            for trend in results["trends"][:3]:
                console.print(f"  • {trend['trend']} (Impact: {trend['impact']})")
            console.print()
        
        # Opportunities
        if results.get("opportunities"):
            console.print("[bold]💡 Strategic Opportunities:[/bold]")
            for opp in results["opportunities"][:2]:
                console.print(f"  • {opp['opportunity']} (Potential: {opp['potential']})")
            console.print()
    
    def _show_learning_insights(self, result: dict):
        """Show learning insights for educational mode"""
        insights = """[bold yellow]🎓 Market Research Insights[/bold yellow]

[green]✓[/green] [bold]Strategic Intelligence:[/bold] Research provides data-driven foundation for product decisions
[green]✓[/green] [bold]Competitive Advantage:[/bold] Understanding market dynamics reveals differentiation opportunities  
[green]✓[/green] [bold]Risk Mitigation:[/bold] Market analysis identifies threats and challenges before they impact you
[green]✓[/green] [bold]Opportunity Discovery:[/bold] Trend analysis uncovers emerging market needs and gaps

[bold]Product Manager Applications:[/bold]
• Use competitive analysis to position your product effectively
• Leverage market trends to prioritize feature development
• Apply market sizing to validate business opportunity size
• Reference industry benchmarks for goal setting and KPIs
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
        if config.get('ticker'):
            cmd_parts = [
                "python shared/market_research.py",
                "--type=company",
                f"--ticker={config['ticker']}",
                f"--experience={config['experience_type']}"
            ]
        else:
            cmd_parts = [
                "python shared/market_research.py",
                "--type=market",
                f"--market-type={config.get('market_type', 'b2b_saas')}",
                f"--industry={config.get('industry', 'technology')}",
                f"--experience={config['experience_type']}"
            ]
        
        if config.get('working_dir', '.') != '.':
            cmd_parts.append(f"--dir=\"{config['working_dir']}\"")
        
        command = " ".join(cmd_parts)
        
        insights = f"""[bold red]🔧 CLI Research Mastery[/bold red]

[bold]Equivalent Command:[/bold]
[blue]{command}[/blue]

[bold]Automation Opportunities:[/bold]
• Schedule regular competitive intelligence reports
• Integrate with CI/CD for market monitoring
• Chain with data analysis tools (pandas, matplotlib)
• Export to business intelligence dashboards

[bold]Advanced Research Techniques:[/bold]
• Combine multiple data sources for comprehensive analysis
• Use APIs for real-time market data integration
• Automate report generation and distribution
• Build custom research workflows and pipelines
"""
        
        cli_panel = Panel(
            insights,
            title="CLI Deep Dive",
            border_style="red",
            padding=(1, 2)
        )
        console.print(cli_panel)

def main(experience_type: Optional[str] = None, research_type: Optional[str] = None):
    """Main CLI entry point"""
    cli_researcher = CLIMarketResearcher()
    
    try:
        console.clear()
        cli_researcher.show_header()
        
        # Select research type if not provided
        if not research_type:
            research_type = cli_researcher.select_research_type()
        
        # Select experience if not provided
        if not experience_type:
            experience_type = cli_researcher.select_experience()
        
        # Configure research
        if research_type == "company":
            config = cli_researcher.configure_company_research(experience_type)
        else:
            config = cli_researcher.configure_market_research(experience_type)
        
        # Conduct research
        result = cli_researcher.conduct_research(config)
        
        # Show results
        cli_researcher.show_results(result, experience_type)
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Research cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - Market Research CLI")
    parser.add_argument("--experience", choices=["just_do_it", "learn_and_do", "cli_deep_dive"],
                       help="Experience type")
    parser.add_argument("--type", choices=["company", "market"], help="Research type")
    
    args = parser.parse_args()
    main(args.experience, args.type)