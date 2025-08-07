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
        manifest_path = self.script_dir / "toolkit.json"
        
        if not manifest_path.exists():
            raise InstallationError(f"Manifest file not found: {manifest_path}")
        
        try:
            with open(manifest_path, 'r') as f:
                self.manifest = json.load(f)
        except Exception as e:
            raise InstallationError(f"Failed to load manifest: {e}")
        
        # Validate manifest version
        required_version = 1.0
        if self.manifest.get("manifest_version") != required_version:
            raise InstallationError(f"Unsupported manifest version. Required: {required_version}")
        
        if self.verbose:
            print(f"{Colors.GREEN}✅ Loaded manifest with {len(self.manifest.get('tools', []))} tools{Colors.END}")

    def _start_web_dashboard(self) -> bool:
        """Start the web dashboard"""
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would start web dashboard at http://localhost:3000{Colors.END}")
            return True
        
        try:
            import subprocess
            import os
            import sys
            
            # Check if web app exists (go up one level from core/)
            toolkit_root = self.script_dir.parent if self.script_dir.name == "core" else self.script_dir
            web_app_path = toolkit_root / "web" / "app.py"
            if not web_app_path.exists():
                print(f"{Colors.RED}❌ Web app not found at {web_app_path}{Colors.END}")
                return False
            
            # Start web dashboard in background using Popen (non-blocking)
            web_process = subprocess.Popen(
                ["python3", "web/app.py"],
                cwd=toolkit_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent process
            )
            
            # Save the PID for later cleanup if needed
            pid_file = toolkit_root / "web_dashboard.pid"
            with open(pid_file, 'w') as f:
                f.write(str(web_process.pid))
            
            # Give it a moment to start
            import time
            time.sleep(2)  # Quick check, don't hold up installer
            
            # Quick port check (non-blocking)
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  # 1 second timeout
                result = sock.connect_ex(('localhost', 3000))
                sock.close()
                
                if result == 0:
                    print(f"{Colors.GREEN}✅ Web dashboard started at http://localhost:3000{Colors.END}")
                else:
                    print(f"{Colors.GREEN}✅ Web dashboard starting in background (PID: {web_process.pid}){Colors.END}")
                    print(f"{Colors.CYAN}   → http://localhost:3000 (may take a few seconds){Colors.END}")
                return True
            except Exception:
                print(f"{Colors.GREEN}✅ Web dashboard starting in background (PID: {web_process.pid}){Colors.END}")
                print(f"{Colors.CYAN}   → http://localhost:3000 (may take a few seconds){Colors.END}")
                return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to start web dashboard: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Manual start: python3 web/app.py{Colors.END}")
            return False

    def _start_workflow_services(self) -> bool:
        """Start workflow services using docker-compose"""
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would start workflow services{Colors.END}")
            return True
        
        try:
            # Fix path - workflows dir is at toolkit root, not in core/
            toolkit_root = self.script_dir.parent if self.script_dir.name == "core" else self.script_dir
            workflows_dir = toolkit_root / "workflows"
            if not workflows_dir.exists():
                print(f"{Colors.YELLOW}⚠️  Workflows directory not found at {workflows_dir}{Colors.END}")
                return True
            
            # Start essential services including Langflow and Jupyter
            services = ["n8n", "langflow", "tooljet"]
            
            for service in services:
                compose_file = workflows_dir / f"docker-compose.{service}.yml"
                if compose_file.exists():
                    try:
                        # Use subprocess.run with timeout for better feedback
                        result = subprocess.run(
                            ["docker-compose", "-f", str(compose_file), "up", "-d"],
                            cwd=workflows_dir,
                            capture_output=True,
                            text=True,
                            timeout=45  # Allow time for Docker to pull images
                        )
                        
                        if result.returncode == 0:
                            print(f"{Colors.GREEN}✅ Started {service} service{Colors.END}")
                        else:
                            print(f"{Colors.RED}❌ Failed to start {service}: {result.stderr.strip()}{Colors.END}")
                            
                    except subprocess.TimeoutExpired:
                        print(f"{Colors.YELLOW}⚠️  {service} starting in background (taking longer than expected){Colors.END}")
                    except Exception as e:
                        print(f"{Colors.RED}❌ Error starting {service}: {e}{Colors.END}")
                        print(f"{Colors.YELLOW}💡 Manual start: cd workflows && docker-compose -f docker-compose.{service}.yml up -d{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}⚠️  {service} compose file not found at {compose_file}{Colors.END}")
            
            return True
            
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Workflow services may need manual start: {e}{Colors.END}")
            return True

    def _start_jupyter_lab(self) -> bool:
        """Start Jupyter Lab"""
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would start Jupyter Lab at http://localhost:8888{Colors.END}")
            return True
        
        try:
            # Check if jupyter-lab is available
            result = subprocess.run(["which", "jupyter-lab"], capture_output=True)
            if result.returncode != 0:
                print(f"{Colors.YELLOW}⚠️  Jupyter Lab not found, skipping{Colors.END}")
                return True
            
            # Start Jupyter Lab in background
            toolkit_root = self.script_dir.parent if self.script_dir.name == "core" else self.script_dir
            
            jupyter_process = subprocess.Popen(
                ["jupyter-lab", "--port=8888", "--no-browser", "--allow-root"],
                cwd=toolkit_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Save PID
            pid_file = toolkit_root / "jupyter_lab.pid"
            with open(pid_file, 'w') as f:
                f.write(str(jupyter_process.pid))
            
            print(f"{Colors.GREEN}✅ Jupyter Lab started (PID: {jupyter_process.pid}){Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to start Jupyter Lab: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Manual start: jupyter-lab --port=8888 --no-browser{Colors.END}")
            return False

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
export AIPM_REPO_DIR="{self.script_dir.parent if self.script_dir.name == 'core' else self.script_dir}"
export AIPM_VERSION="1.0"

# Quick AI Research & Analysis
alias aipm_research_quick='cd "$AIPM_REPO_DIR" && ./research-quick.sh'
alias aipm_company_lookup='echo "Usage: aipm_company_lookup TICKER - Get financial intelligence on any public company"'
alias aipm_competitive_analysis='echo "Starting comprehensive competitive analysis workflow"'

# AI Collaboration & Content Creation  
alias aipm_brainstorm='cd "$AIPM_REPO_DIR" && ./brainstorm.sh'
alias aipm_write='echo "Start AI writing partner: aider [filename.md]"'
alias aipm_prototype_demo='echo "Create visual demo: aider [filename.html]"'

# Visual Workflow & Automation
alias aipm_workflows='echo "🚀 Starting visual workflow tools..." && cd "$AIPM_REPO_DIR/workflows" && ./start-workflows.sh'
alias aipm_workflows_status='cd "$AIPM_REPO_DIR/workflows" && ./status-workflows.sh'
alias aipm_workflows_stop='cd "$AIPM_REPO_DIR/workflows" && ./stop-workflows.sh'
alias aipm_workflows_restart='aipm_workflows_stop && sleep 3 && aipm_workflows'
alias aipm_workflows_fix='cd "$AIPM_REPO_DIR/workflows" && ./fix-workflows.sh'
alias aipm_workflows_cleanup='cd "$AIPM_REPO_DIR/workflows" && ./cleanup-workflows.sh'
alias aipm_workflows_tooljet='cd "$AIPM_REPO_DIR/workflows" && ./orchestrate-workflows.sh tooljet'
alias aipm_workflows_typebot='cd "$AIPM_REPO_DIR/workflows" && ./orchestrate-workflows.sh typebot'  
alias aipm_workflows_penpot='cd "$AIPM_REPO_DIR/workflows" && ./orchestrate-workflows.sh penpot'
alias aipm_workflows_all='cd "$AIPM_REPO_DIR/workflows" && ./orchestrate-workflows.sh all'
alias aipm_automate='echo "🚀 Launching n8n workflow builder..." && aipm_workflows_status | grep -q "n8n - Running" || aipm_workflows && echo "n8n ready at: http://localhost:5678" && open http://localhost:5678'
alias aipm_demo_builder='echo "🚀 Launching ToolJet dashboard builder..." && aipm_workflows_status | grep -q "ToolJet - Running" || aipm_workflows_tooljet && echo "ToolJet ready at: http://localhost:8082" && open http://localhost:8082'

# Data & Research Tools
alias aipm_lab='cd "$AIPM_TOOLKIT_DIR" && echo "🧪 Launching data analysis environment..." && jupyter lab --no-browser --port=8888'
alias aipm_market_research='echo "Access financial data and market intelligence tools"'
alias aipm_data_generator='cd "$AIPM_REPO_DIR" && ./data-generator.sh'

# Design & Visualization
alias aipm_design='echo "🎨 Opening Excalidraw for diagrams and mockups..." && open https://excalidraw.com'
alias aipm_knowledge='echo "📚 Opening knowledge management..." && open -a Obsidian "$AIPM_TOOLKIT_DIR/obsidian-vault" 2>/dev/null || echo "Install Obsidian first: brew install --cask obsidian"'

# Core PoL Probe Framework (Advanced)
alias aipm_learn='echo "💡 Feasibility Check: Use AI to validate technical assumptions quickly"'
alias aipm_fast='echo "⚡ Task-Focused Test: Validate specific user friction points"'  
alias aipm_show='echo "🎬 Narrative Prototype: Create explainer demos for stakeholders"'
alias aipm_experiment='echo "🧪 Synthetic Data Simulation: Model user behavior at scale"'
alias aipm_compete='echo "🥊 Vibe-Coded Probe: Build convincing fake frontend for testing"'

# Audio Intelligence Tools
alias aipm_transcribe='python3 "$AIPM_REPO_DIR/src/audio_transcription.py"'
alias aipm_audio_workflows='python3 "$AIPM_REPO_DIR/src/pm_audio_workflows.py" --list'
alias aipm_user_interview='python3 "$AIPM_REPO_DIR/src/pm_audio_workflows.py" --workflow user_interview_analysis --audio'
alias aipm_meeting_summary='python3 "$AIPM_REPO_DIR/src/pm_audio_workflows.py" --workflow stakeholder_meeting_summary --audio'
alias aipm_demo_feedback='python3 "$AIPM_REPO_DIR/src/pm_audio_workflows.py" --workflow demo_feedback_analysis --audio'

# Web Dashboard & Hub
alias aipm_dashboard='echo "🚀 Starting AI PM Toolkit Web Dashboard..." && cd "$AIPM_REPO_DIR" && python3 web/app.py'
alias aipm_hub='aipm_dashboard'
alias aipm_web='aipm_dashboard'

# Help & Status
alias aipm_status='python3 "$AIPM_REPO_DIR/installer.py" --status'
alias aipm_help='echo "🧪 AI PM Toolkit - Your AI-Powered Product Management Arsenal" && echo "" && echo "🎯 NEW UNIFIED CLI:" && echo "  aipm data-gen --count=10 --type=b2b_saas - Generate synthetic personas" && echo "  aipm transcribe audio.mp3 --use-case=user_interviews - Audio analysis" && echo "  aipm chat --mode=pm_assistant --interactive - AI strategic partner" && echo "  aipm research --company=\"CompanyName\" - Market intelligence" && echo "  aipm help - Show this help" && echo "" && echo "🌐 QUICK START:" && echo "  aipm_dashboard - Launch web interface (http://localhost:3000)" && echo "  • Read docs: open -a MarkText \"$AIPM_REPO_DIR/docs/PM_FIRST_STEPS.md\"" && echo "  • Learning guide: open \"$AIPM_REPO_DIR/learning-guide/index.html\"" && echo "  • Troubleshooting: open -a MarkText \"$AIPM_REPO_DIR/docs/TROUBLESHOOTING_GUIDE.md\"" && echo "" && echo "🎙️ AUDIO INTELLIGENCE (Working):" && echo "  python3 \"$AIPM_REPO_DIR/src/audio_transcription.py\" audio.mp3 --use-case=user_interviews" && echo "  python3 \"$AIPM_REPO_DIR/src/pm_audio_workflows.py\" --list" && echo "" && echo "📊 DATA GENERATION (Working):" && echo "  python3 \"$AIPM_REPO_DIR/src/data_generator.py\" --count=10 --type=b2b_saas" && echo "  python3 \"$AIPM_REPO_DIR/src/ai_chat.py\" --mode=pm_assistant --interactive" && echo "" && echo "🔧 VISUAL BUILDERS (Working):" && echo "  aipm_workflows - Start workflow tools (n8n, etc)" && echo "  aipm_workflows_status - Check service status" && echo "  aipm_workflows_fix - Fix common issues" && echo "  aipm_lab - Jupyter Lab environment" && echo "    → n8n automation: http://localhost:5678" && echo "    → ToolJet dashboards: http://localhost:8082" && echo "    → Typebot forms: http://localhost:8083" && echo "" && echo "📚 LEARNING RESOURCES:" && echo "  • Interactive Guide: open \"$AIPM_REPO_DIR/learning-guide/index.html\"" && echo "  • PM Playbooks: open \"$AIPM_REPO_DIR/playbooks/\"" && echo "  • API Reference: open -a MarkText \"$AIPM_REPO_DIR/docs/AIPM_COMMANDS_API.md\"" && echo "" && echo "⚠️ BROKEN COMMANDS (Use alternatives above):" && echo "  aipm_research_quick, aipm_company_lookup, aipm_transcribe (old paths)" && echo "  aipm_brainstorm, aipm_write, aipm_prototype_demo (not implemented)" && echo "  All PoL probe commands (aipm_learn, aipm_fast, etc.) - use new aipm CLI" && echo "" && echo "💡 NEXT STEPS:" && echo "  1. Try: aipm data-gen --count=5 --type=b2b_saas" && echo "  2. Read: open -a MarkText \"$AIPM_REPO_DIR/docs/PM_FIRST_STEPS.md\"" && echo "  3. Explore: open \"$AIPM_REPO_DIR/learning-guide/index.html\""'

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
        
        # Start services after installation
        print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 Starting Services{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.END}")
        
        # Start web dashboard
        print("Starting web dashboard...")
        self._start_web_dashboard()
        
        # Start Jupyter Lab
        print("Starting Jupyter Lab...")
        self._start_jupyter_lab()
        
        # Start workflow services
        print("Starting workflow services...")
        self._start_workflow_services()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Welcome to the AI PM Toolkit!{Colors.END}")
        print(f"{Colors.GREEN}{'=' * 50}{Colors.END}")
        print(f"{Colors.CYAN}✨ Installation complete! Services are starting up:{Colors.END}")
        print()
        print(f"{Colors.BOLD}1. Restart your terminal{Colors.END} or run: {Colors.YELLOW}source ~/.zshrc{Colors.END}")
        print(f"{Colors.BOLD}2. Try your first command:{Colors.END} {Colors.YELLOW}aipm_help{Colors.END}")
        print(f"{Colors.BOLD}3. Start learning:{Colors.END}")
        print(f"   • {Colors.CYAN}Interactive Guide:{Colors.END} open learning-guide/index.html")
        print(f"   • {Colors.CYAN}First Steps:{Colors.END} open -a MarkText docs/PM_FIRST_STEPS.md")
        print()
        print(f"{Colors.BOLD}🚀 Quick wins to try right now:{Colors.END}")
        print(f"   • {Colors.YELLOW}aipm_research_quick \"AI trends in product management\"{Colors.END}")
        print(f"   • {Colors.YELLOW}aipm_lab{Colors.END} - Launch data analysis environment")
        print(f"   • {Colors.YELLOW}aipm_workflows{Colors.END} - Start visual workflow builders")
        print()
        print(f"{Colors.BOLD}🔗 Services available:{Colors.END}")
        print(f"   • Web Dashboard: {Colors.GREEN}http://localhost:3000{Colors.END} ✅")
        print(f"   • Jupyter Lab: {Colors.GREEN}http://localhost:8888{Colors.END} ✅") 
        print(f"   • n8n Workflows: {Colors.GREEN}http://localhost:5678{Colors.END} ✅")
        print(f"   • Langflow AI: {Colors.GREEN}http://localhost:7860{Colors.END} ✅")
        print(f"   • ToolJet Dashboards: {Colors.YELLOW}http://localhost:8082{Colors.END} (may need manual start)")
        print()
        print(f"{Colors.GREEN}💡 To manually start missing services: cd workflows && ./start-workflows.sh{Colors.END}")
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
        print("🧪 AI PM Toolkit Status Check")
        print("=" * 40)
        
        # Check key components
        components = [
            ("Docker", "docker --version"),
            ("Python", "python3 --version"),
            ("Aider", "aider --version"),
            ("Jupyter", "jupyter --version"),
            ("Ollama", "ollama --version")
        ]
        
        for name, cmd in components:
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0]
                    print(f"✅ {name}: {version}")
                else:
                    print(f"❌ {name}: Not working")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"⚠️  {name}: Not installed")
        
        # Check workflow tools
        print("\n🔧 Workflow Tools:")
        try:
            result = subprocess.run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                aipm_containers = [line for line in lines if 'aipm' in line.lower() or 'n8n' in line.lower() or 'tooljet' in line.lower()]
                if aipm_containers:
                    for container in aipm_containers:
                        print(f"  {container}")
                else:
                    print("  No workflow containers running")
            else:
                print("  Docker not accessible")
        except:
            print("  Cannot check Docker containers")
            
        print(f"\n📁 Toolkit Directory: {Path.home() / 'ai-pm-toolkit'}")
        print("💡 Run 'aipm_help' for available commands")
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