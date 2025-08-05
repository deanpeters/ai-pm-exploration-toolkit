#!/usr/bin/env python3
"""
AI PM Exploration Toolkit - Production Installer
Resilient, cross-platform installer with dependency management and comprehensive error handling.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class InstallationError(Exception):
    """Custom exception for installation failures"""
    pass


class ToolkitInstaller:
    """Main installer class for AI PM Toolkit"""
    
    def __init__(self, tier: int = 1, dry_run: bool = False, verbose: bool = False):
        self.tier = tier
        self.dry_run = dry_run
        self.verbose = verbose
        self.manifest = {}
        self.platform = self._detect_platform()
        self.results = []
        self.toolkit_dir = Path.home() / "ai-pm-toolkit"
        self.script_dir = Path(__file__).parent.absolute()
        
        print(f"{Colors.CYAN}{Colors.BOLD}🧪 AI PM Exploration Toolkit Installer{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.END}")
        print(f"Platform: {Colors.YELLOW}{self.platform}{Colors.END}")
        print(f"Tier: {Colors.YELLOW}{tier} ({'Essentials' if tier == 1 else 'Advanced' if tier == 2 else 'Full'}){Colors.END}")
        if dry_run:
            print(f"{Colors.YELLOW}🔍 DRY RUN MODE - No changes will be made{Colors.END}")
        print()

    def _detect_platform(self) -> str:
        """Detect the current platform"""
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        elif system == "linux":
            return "linux"
        elif system == "windows":
            return "windows"
        else:
            raise InstallationError(f"Unsupported platform: {system}")

    def _load_manifest(self) -> None:
        """Load and validate the toolkit manifest"""
        manifest_path = self.script_dir / "toolkit.yaml"
        
        if not manifest_path.exists():
            raise InstallationError(f"Manifest file not found: {manifest_path}")
        
        try:
            with open(manifest_path, 'r') as f:
                self.manifest = yaml.safe_load(f)
        except Exception as e:
            raise InstallationError(f"Failed to load manifest: {e}")
        
        # Validate manifest version
        required_version = 1.0
        if self.manifest.get("manifest_version") != required_version:
            raise InstallationError(f"Unsupported manifest version. Required: {required_version}")
        
        if self.verbose:
            print(f"{Colors.GREEN}✅ Loaded manifest with {len(self.manifest.get('tools', []))} tools{Colors.END}")

    def _run_command(self, command: str, timeout: int = 300) -> Tuple[bool, str]:
        """Execute a command with timeout and error handling"""
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would execute: {command}{Colors.END}")
            return True, "dry-run-success"
        
        try:
            if self.verbose:
                print(f"{Colors.BLUE}Executing: {command}{Colors.END}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
                
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, str(e)

    def _check_tool_installed(self, tool: Dict) -> bool:
        """Check if a tool is already installed"""
        platform_config = tool.get("platforms", {}).get(self.platform)
        if not platform_config:
            return False
        
        check_command = platform_config.get("check_command")
        if not check_command:
            return False
        
        success, _ = self._run_command(check_command)
        return success

    def _install_with_brew(self, package_name: str, is_cask: bool = False) -> Tuple[bool, str]:
        """Install package using Homebrew"""
        if not self._check_command_exists("brew"):
            return False, "Homebrew not found. Please install Homebrew first."
        
        cask_flag = "--cask" if is_cask else ""
        command = f"brew install {cask_flag} {package_name}"
        return self._run_command(command)

    def _install_with_apt(self, package_name: str) -> Tuple[bool, str]:
        """Install package using apt (Linux)"""
        if not self._check_command_exists("apt"):
            return False, "apt package manager not found"
        
        # Update package list first
        self._run_command("sudo apt update")
        command = f"sudo apt install -y {package_name}"
        return self._run_command(command)

    def _install_with_pip(self, package_name: str) -> Tuple[bool, str]:
        """Install package using pip"""
        if not self._check_command_exists("pip3") and not self._check_command_exists("pip"):
            return False, "pip not found. Please install Python first."
        
        pip_cmd = "pip3" if self._check_command_exists("pip3") else "pip"
        command = f"{pip_cmd} install {package_name}"
        return self._run_command(command)

    def _install_with_npm(self, package_name: str) -> Tuple[bool, str]:
        """Install package using npm"""
        if not self._check_command_exists("npm"):
            return False, "npm not found. Please install Node.js first."
        
        command = f"npm install -g {package_name}"
        return self._run_command(command)

    def _install_vscode_extension(self, extension_id: str) -> Tuple[bool, str]:
        """Install VS Code extension"""
        if not self._check_command_exists("code"):
            return False, "VS Code not found. Please install VS Code first."
        
        command = f"code --install-extension {extension_id}"
        return self._run_command(command)

    def _install_with_docker(self, image: str) -> Tuple[bool, str]:
        """Pull Docker image"""
        if not self._check_command_exists("docker"):
            return False, "Docker not found. Please install Docker first."
        
        command = f"docker pull {image}"
        return self._run_command(command)

    def _install_with_docker_compose(self, config_file: str) -> Tuple[bool, str]:
        """Start service using Docker Compose"""
        if not self._check_command_exists("docker-compose") and not self._check_command_exists("docker compose"):
            return False, "Docker Compose not found"
        
        config_path = self.script_dir / config_file
        if not config_path.exists():
            return False, f"Docker Compose file not found: {config_path}"
        
        compose_cmd = "docker compose" if self._check_command_exists("docker compose") else "docker-compose"
        command = f"cd {config_path.parent} && {compose_cmd} -f {config_path.name} up -d"
        return self._run_command(command)

    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        success, _ = self._run_command(f"which {command}" if self.platform != "windows" else f"where {command}")
        return success

    def _install_tool(self, tool: Dict) -> Dict:
        """Install a single tool"""
        name = tool.get("name", "unknown")
        description = tool.get("description", "")
        
        result = {
            "name": name,
            "description": description,
            "status": "unknown",
            "message": "",
            "skipped": False
        }
        
        # Check if tool is already installed
        if self._check_tool_installed(tool):
            result["status"] = "already_installed"
            result["message"] = "Already installed"
            result["skipped"] = True
            return result
        
        # Get platform-specific configuration
        platform_config = tool.get("platforms", {}).get(self.platform)
        if not platform_config:
            result["status"] = "unsupported"
            result["message"] = f"Not supported on {self.platform}"
            return result
        
        installer = platform_config.get("installer")
        
        try:
            success = False
            message = ""
            
            if installer == "brew":
                success, message = self._install_with_brew(platform_config.get("package_name"))
            elif installer == "brew-cask":
                success, message = self._install_with_brew(platform_config.get("package_name"), is_cask=True)
            elif installer == "apt":
                success, message = self._install_with_apt(platform_config.get("package_name"))
            elif installer == "pip":
                success, message = self._install_with_pip(platform_config.get("package_name"))
            elif installer == "npm":
                success, message = self._install_with_npm(platform_config.get("package_name"))
            elif installer == "vscode-extension":
                success, message = self._install_vscode_extension(platform_config.get("extension_id"))
            elif installer == "docker":
                success, message = self._install_with_docker(platform_config.get("image"))
            elif installer == "docker-compose":
                success, message = self._install_with_docker_compose(platform_config.get("config_file"))
            elif installer == "curl":
                success, message = self._run_command(platform_config.get("install_script"))
            elif installer == "web":
                result["status"] = "web_based"
                result["message"] = f"Web-based tool: {platform_config.get('url')}"
                return result
            elif installer == "manual":
                result["status"] = "manual"
                result["message"] = f"Manual installation required: {platform_config.get('url')}"
                return result
            else:
                result["status"] = "unsupported_installer"
                result["message"] = f"Unsupported installer: {installer}"
                return result
            
            if success:
                # Verify installation
                if self._check_tool_installed(tool):
                    result["status"] = "success"
                    result["message"] = "Installed successfully"
                else:
                    result["status"] = "verification_failed"
                    result["message"] = "Installation completed but verification failed"
            else:
                result["status"] = "failed"
                result["message"] = message or "Installation failed"
                
        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
        
        return result

    def _resolve_dependencies(self, tools: List[Dict]) -> List[Dict]:
        """Resolve tool dependencies and return sorted list"""
        # Create dependency graph
        tool_map = {tool["name"]: tool for tool in tools}
        resolved = []
        resolving = set()
        
        def resolve_tool(tool_name: str) -> None:
            if tool_name in resolved:
                return
            if tool_name in resolving:
                raise InstallationError(f"Circular dependency detected: {tool_name}")
            
            resolving.add(tool_name)
            tool = tool_map.get(tool_name)
            if tool:
                # Resolve dependencies first
                for dep in tool.get("depends_on", []):
                    if dep in tool_map:
                        resolve_tool(dep)
                
                if tool_name not in [t["name"] for t in resolved]:
                    resolved.append(tool)
            
            resolving.remove(tool_name)
        
        # Resolve all tools
        for tool in tools:
            resolve_tool(tool["name"])
        
        return resolved

    def _create_environment_script(self) -> None:
        """Create the aipm-env.sh script with toolkit environment"""
        env_script_path = self.toolkit_dir / "aipm-env.sh"
        
        # Create toolkit directory if it doesn't exist
        self.toolkit_dir.mkdir(exist_ok=True)
        
        env_content = f"""#!/bin/bash
# AI PM Toolkit Environment
# Generated by installer.py on {time.strftime('%Y-%m-%d %H:%M:%S')}

export AIPM_TOOLKIT_DIR="{self.toolkit_dir}"
export AIPM_VERSION="1.0"

# Quick AI Research & Analysis
alias aipm_research_quick='echo "Usage: aipm_research_quick \"your research question\" - Get instant expert analysis"'
alias aipm_company_lookup='echo "Usage: aipm_company_lookup TICKER - Get financial intelligence on any public company"'
alias aipm_competitive_analysis='echo "Starting comprehensive competitive analysis workflow"'

# AI Collaboration & Content Creation  
alias aipm_brainstorm='aider'
alias aipm_write='echo "Start AI writing partner: aider [filename.md]"'
alias aipm_prototype_demo='echo "Create visual demo: aider [filename.html]"'

# Visual Workflow & Automation
alias aipm_workflows='echo "🚀 Starting visual workflow tools..." && echo "n8n: http://localhost:5678 | Langflow: http://localhost:7860 | ToolJet: http://localhost:8082"'
alias aipm_automate='echo "Launch n8n workflow builder: http://localhost:5678"'
alias aipm_demo_builder='echo "Launch ToolJet dashboard builder: http://localhost:8082"'

# Data & Research Tools
alias aipm_lab='cd "$AIPM_TOOLKIT_DIR" && echo "🧪 Launching data analysis environment..." && jupyter lab --no-browser --port=8888'
alias aipm_market_research='echo "Access financial data and market intelligence tools"'
alias aipm_data_generator='echo "Generate synthetic data for testing and validation"'

# Design & Visualization
alias aipm_design='echo "🎨 Opening Excalidraw for diagrams and mockups..." && open https://excalidraw.com'
alias aipm_knowledge='echo "📚 Opening knowledge management..." && open -a Obsidian "$AIPM_TOOLKIT_DIR/obsidian-vault" 2>/dev/null || echo "Install Obsidian first: brew install --cask obsidian"'

# Core PoL Probe Framework (Advanced)
alias aipm_learn='echo "💡 Feasibility Check: Use AI to validate technical assumptions quickly"'
alias aipm_fast='echo "⚡ Task-Focused Test: Validate specific user friction points"'  
alias aipm_show='echo "🎬 Narrative Prototype: Create explainer demos for stakeholders"'
alias aipm_experiment='echo "🧪 Synthetic Data Simulation: Model user behavior at scale"'
alias aipm_compete='echo "🥊 Vibe-Coded Probe: Build convincing fake frontend for testing"'

# Help & Status
alias aipm_status='python3 "$AIPM_TOOLKIT_DIR/../installer.py" --status'
alias aipm_help='echo "🧪 AI PM Toolkit - Your AI-Powered Product Management Arsenal" && echo "" && echo "🎯 QUICK START:" && echo "  • Read docs/PM_FIRST_STEPS.md - Your guided first experience" && echo "  • Visit learning-guide/index.html - Interactive learning tracks" && echo "  • Join the toolkit Slack community for tips & examples" && echo "" && echo "🔍 RESEARCH & INTELLIGENCE:" && echo "  aipm_research_quick \"question\" - Instant expert analysis" && echo "  aipm_company_lookup TICKER - Financial intelligence on any public company" && echo "  aipm_market_research - Launch comprehensive research tools" && echo "" && echo "✍️ AI COLLABORATION:" && echo "  aipm_brainstorm - Start AI pair programming session" && echo "  aipm_write filename.md - Co-create documents with AI" && echo "  aipm_prototype_demo - Build interactive demos with AI" && echo "" && echo "🔧 VISUAL BUILDERS (with direct links):" && echo "  aipm_workflows - Launch all workflow tools" && echo "    → n8n automation: http://localhost:5678" && echo "    → Langflow visual AI: http://localhost:7860" && echo "    → ToolJet dashboards: http://localhost:8082" && echo "    → Typebot chatbots: http://localhost:3001" && echo "" && echo "📊 DATA & ANALYSIS:" && echo "  aipm_lab - Jupyter Lab data environment (http://localhost:8888)" && echo "  aipm_data_generator - Create synthetic test data" && echo "  • OpenBB Terminal - Financial data (openbb-terminal)" && echo "" && echo "🎨 DESIGN & KNOWLEDGE:" && echo "  aipm_design - Create diagrams (opens Excalidraw)" && echo "  aipm_knowledge - Knowledge management (opens Obsidian vault)" && echo "" && echo "⚡ POL PROBE FRAMEWORK:" && echo "  aipm_learn - Feasibility checks (1-2 day technical spikes)" && echo "  aipm_fast - Task-focused tests (validate specific user friction)" && echo "  aipm_show - Narrative prototypes (stakeholder demo creation)" && echo "  aipm_experiment - Synthetic data simulations (wind tunnel testing)" && echo "  aipm_compete - Vibe-coded probes (fake frontend + backend)" && echo "" && echo "📚 LEARNING RESOURCES:" && echo "  • Interactive Guide: learning-guide/index.html" && echo "  • PM Playbooks: Check playbooks/ directory" && echo "  • Tool Documentation: Each tool has help flags (-h, --help)" && echo "  • Community: Slack workspace for sharing examples" && echo "" && echo "🚨 TROUBLESHOOTING:" && echo "  • Port conflicts? Kill processes: sudo lsof -ti:PORT | xargs kill" && echo "  • Tool not found? Check installation: aipm_status" && echo "  • Docker issues? Restart: docker system prune && docker-compose up" && echo "" && echo "💡 NEXT STEPS: Start with docs/PM_FIRST_STEPS.md or learning-guide/index.html"'

echo "🧪 AI PM Toolkit environment loaded"
echo "Type 'aipm_help' for available commands"
"""
        
        if not self.dry_run:
            with open(env_script_path, 'w') as f:
                f.write(env_content)
            env_script_path.chmod(0o755)
            
            if self.verbose:
                print(f"{Colors.GREEN}✅ Created environment script: {env_script_path}{Colors.END}")

    def _setup_shell_integration(self) -> None:
        """Safely add source command to user's shell config"""
        env_script_path = self.toolkit_dir / "aipm-env.sh"
        source_line = f'source "{env_script_path}"'
        
        # Detect user's shell
        shell = os.environ.get('SHELL', '/bin/bash')
        shell_name = Path(shell).name
        
        # Determine config file
        config_files = {
            'bash': ['.bashrc', '.bash_profile'],
            'zsh': ['.zshrc'],
            'fish': ['.config/fish/config.fish'],
        }
        
        config_paths = []
        for config_file in config_files.get(shell_name, ['.bashrc']):
            config_paths.append(Path.home() / config_file)
        
        # Find existing config file or use the first one
        existing_config = None
        for config_path in config_paths:
            if config_path.exists():
                existing_config = config_path
                break
        
        if not existing_config:
            existing_config = config_paths[0]
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would add source line to: {existing_config}{Colors.END}")
            return
        
        # Check if source line already exists
        try:
            if existing_config.exists():
                with open(existing_config, 'r') as f:
                    content = f.read()
                if source_line in content:
                    if self.verbose:
                        print(f"{Colors.GREEN}✅ Shell integration already configured in {existing_config}{Colors.END}")
                    return
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Could not read {existing_config}: {e}{Colors.END}")
        
        # Add source line
        try:
            with open(existing_config, 'a') as f:
                f.write(f"\n# AI PM Toolkit Environment\n{source_line}\n")
            
            print(f"{Colors.GREEN}✅ Added shell integration to {existing_config}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Restart your terminal or run: source {existing_config}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to add shell integration: {e}{Colors.END}")

    def _print_summary(self) -> None:
        """Print installation summary"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}📊 Installation Summary{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.END}")
        
        # Count results by status
        status_counts = {}
        for result in self.results:
            status = result["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Print status summary
        status_colors = {
            "success": Colors.GREEN,
            "already_installed": Colors.BLUE,
            "failed": Colors.RED,
            "error": Colors.RED,
            "manual": Colors.YELLOW,
            "web_based": Colors.CYAN,
            "unsupported": Colors.MAGENTA,
            "verification_failed": Colors.YELLOW,
        }
        
        for status, count in status_counts.items():
            color = status_colors.get(status, Colors.WHITE)
            print(f"{color}{status.replace('_', ' ').title()}: {count}{Colors.END}")
        
        # Print detailed results
        print(f"\n{Colors.BOLD}Detailed Results:{Colors.END}")
        for result in self.results:
            status = result["status"]
            color = status_colors.get(status, Colors.WHITE)
            
            if result["skipped"]:
                icon = "⏭️ "
            elif status == "success":
                icon = "✅"
            elif status in ["failed", "error"]:
                icon = "❌"
            elif status in ["manual", "web_based"]:
                icon = "💡"
            else:
                icon = "ℹ️ "
            
            print(f"{icon} {Colors.BOLD}{result['name']}{Colors.END}: {color}{result['message']}{Colors.END}")
        
        # Print next steps
        print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 Next Steps{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.END}")
        
        manual_tools = [r for r in self.results if r["status"] == "manual"]
        if manual_tools:
            print(f"{Colors.YELLOW}Manual installations required:{Colors.END}")
            for tool in manual_tools:
                print(f"  • {tool['name']}: {tool['message']}")
        
        failed_tools = [r for r in self.results if r["status"] in ["failed", "error"]]
        if failed_tools:
            print(f"{Colors.RED}Failed installations (check logs):{Colors.END}")
            for tool in failed_tools:
                print(f"  • {tool['name']}: {tool['message']}")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Welcome to the AI PM Toolkit!{Colors.END}")
        print(f"{Colors.GREEN}{'=' * 50}{Colors.END}")
        print(f"{Colors.CYAN}✨ Installation complete! Here's how to get started:{Colors.END}")
        print()
        print(f"{Colors.BOLD}1. Restart your terminal{Colors.END} or run: {Colors.YELLOW}source ~/.zshrc{Colors.END}")
        print(f"{Colors.BOLD}2. Try your first command:{Colors.END} {Colors.YELLOW}aipm_help{Colors.END}")
        print(f"{Colors.BOLD}3. Start learning:{Colors.END}")
        print(f"   • {Colors.CYAN}Interactive Guide:{Colors.END} open learning-guide/index.html")
        print(f"   • {Colors.CYAN}First Steps:{Colors.END} cat docs/PM_FIRST_STEPS.md")
        print()
        print(f"{Colors.BOLD}🚀 Quick wins to try right now:{Colors.END}")
        print(f"   • {Colors.YELLOW}aipm_research_quick \"AI trends in product management\"{Colors.END}")
        print(f"   • {Colors.YELLOW}aipm_lab{Colors.END} - Launch data analysis environment")
        print(f"   • {Colors.YELLOW}aipm_workflows{Colors.END} - Start visual workflow builders")
        print()
        print(f"{Colors.BOLD}🔗 Direct tool access:{Colors.END}")
        print(f"   • Jupyter Lab: {Colors.BLUE}http://localhost:8888{Colors.END}")
        print(f"   • n8n Workflows: {Colors.BLUE}http://localhost:5678{Colors.END}")
        print(f"   • Langflow AI: {Colors.BLUE}http://localhost:7860{Colors.END}")
        print(f"   • ToolJet Dashboards: {Colors.BLUE}http://localhost:8082{Colors.END}")
        print()
        print(f"{Colors.YELLOW}💡 Tip: Run {Colors.BOLD}aipm_help{Colors.END}{Colors.YELLOW} anytime for the complete command reference!{Colors.END}")

    def install(self) -> None:
        """Main installation process"""
        try:
            # Load manifest
            self._load_manifest()
            
            # Filter tools by tier
            all_tools = self.manifest.get("tools", [])
            filtered_tools = [
                tool for tool in all_tools 
                if tool.get("tier", 1) <= self.tier
            ]
            
            print(f"Installing {len(filtered_tools)} tools for Tier {self.tier}...")
            
            # Resolve dependencies
            ordered_tools = self._resolve_dependencies(filtered_tools)
            
            # Install tools
            for i, tool in enumerate(ordered_tools, 1):
                name = tool.get("name", "unknown")
                print(f"\n[{i}/{len(ordered_tools)}] Installing {Colors.BOLD}{name}{Colors.END}...")
                
                result = self._install_tool(tool)
                self.results.append(result)
                
                # Print immediate result
                if result["skipped"]:
                    print(f"  ⏭️ {Colors.BLUE}{result['message']}{Colors.END}")
                elif result["status"] == "success":
                    print(f"  ✅ {Colors.GREEN}{result['message']}{Colors.END}")
                elif result["status"] in ["failed", "error"]:
                    print(f"  ❌ {Colors.RED}{result['message']}{Colors.END}")
                else:
                    print(f"  ℹ️  {Colors.YELLOW}{result['message']}{Colors.END}")
            
            # Create environment
            print(f"\n{Colors.CYAN}Setting up toolkit environment...{Colors.END}")
            self._create_environment_script()
            self._setup_shell_integration()
            
            # Print summary
            self._print_summary()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Installation interrupted by user{Colors.END}")
            sys.exit(1)
        except Exception as e:
            print(f"\n{Colors.RED}Installation failed: {e}{Colors.END}")
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI PM Exploration Toolkit - Production Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tier Levels:
  1 (essentials) - Core PoL Probe capabilities (15-20 min)
  2 (advanced)   - Deeper capabilities with testing tools (30-45 min)  
  3 (full)       - Expert tools and AI observability (60-90 min)

Examples:
  python installer.py --tier 1
  python installer.py --tier 2 --verbose
  python installer.py --tier 3 --dry-run
        """
    )
    
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Installation tier (1=essentials, 2=advanced, 3=full)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making changes"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show installation status"
    )
    
    args = parser.parse_args()
    
    if args.status:
        print("🧪 AI PM Toolkit Status Check - Not implemented yet")
        return
    
    # Create and run installer
    installer = ToolkitInstaller(
        tier=args.tier,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    installer.install()


if __name__ == "__main__":
    main()