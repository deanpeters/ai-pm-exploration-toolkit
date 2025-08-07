#!/usr/bin/env python3
"""
AI PM Toolkit - Jupyter Lab Integration
Data exploration and analysis workspace for product managers
"""

import json
import os
import subprocess
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class JupyterConfig:
    """Configuration for Jupyter Lab session"""
    port: int = 8888
    working_dir: str = "."
    notebook_dir: str = "notebooks"
    auto_open_browser: bool = True
    enable_extensions: bool = True
    allow_external_access: bool = False
    session_name: str = "aipm_data_exploration"

class JupyterLabManager:
    """Manager for Jupyter Lab sessions and notebooks"""
    
    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.jupyter_process = None
        self.config = None
        
    def check_jupyter_availability(self) -> Dict[str, Any]:
        """Check if Jupyter Lab and required packages are available"""
        availability = {
            "jupyter": False,
            "jupyterlab": False,
            "pandas": False,
            "matplotlib": False,
            "seaborn": False,
            "plotly": False,
            "version_info": {}
        }
        
        # Check Jupyter
        try:
            result = subprocess.run(['jupyter', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                availability["jupyter"] = True
                availability["version_info"]["jupyter"] = result.stdout.strip()
        except:
            pass
        
        # Check JupyterLab
        try:
            result = subprocess.run(['jupyter-lab', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                availability["jupyterlab"] = True
                availability["version_info"]["jupyterlab"] = result.stdout.strip()
        except:
            pass
        
        # Check required packages
        packages = ["pandas", "matplotlib", "seaborn", "plotly"]
        for package in packages:
            try:
                __import__(package)
                availability[package] = True
            except ImportError:
                availability[package] = False
        
        return availability
    
    def setup_jupyter_environment(self, config: JupyterConfig) -> Dict[str, Any]:
        """Set up Jupyter environment with PM-specific configurations"""
        
        # Create notebook directory
        notebook_dir = self.working_dir / config.notebook_dir
        notebook_dir.mkdir(exist_ok=True)
        
        # Create PM-specific subdirectories
        subdirs = [
            "market_research",
            "user_data_analysis", 
            "synthetic_data_experiments",
            "competitive_analysis",
            "templates"
        ]
        
        for subdir in subdirs:
            (notebook_dir / subdir).mkdir(exist_ok=True)
        
        # Create starter templates
        self._create_template_notebooks(notebook_dir)
        
        # Create Jupyter config if needed
        self._setup_jupyter_config(config)
        
        return {
            "notebook_dir": str(notebook_dir),
            "templates_created": len(subdirs),
            "config_file": "jupyter_lab_config.py"
        }
    
    def _create_template_notebooks(self, notebook_dir: Path):
        """Create template notebooks for PM use cases"""
        
        templates = {
            "templates/PM_Market_Research_Template.ipynb": self._get_market_research_template(),
            "templates/PM_User_Data_Analysis.ipynb": self._get_user_data_template(),
            "templates/PM_Synthetic_Data_Generation.ipynb": self._get_synthetic_data_template(),
            "templates/PM_Competitive_Analysis.ipynb": self._get_competitive_analysis_template()
        }
        
        for template_path, template_content in templates.items():
            full_path = notebook_dir / template_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(template_content, f, indent=2)
    
    def _get_market_research_template(self) -> Dict:
        """Generate market research template notebook"""
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 📊 Product Manager Market Research Template\n",
                        "\n",
                        "This notebook template helps PMs conduct data-driven market research using the AI PM Toolkit.\n",
                        "\n",
                        "## 🎯 Use Cases\n",
                        "- Competitor financial analysis\n",
                        "- Market trend identification\n",
                        "- Industry benchmarking\n",
                        "- Investment thesis validation\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Import required libraries\n",
                        "import pandas as pd\n",
                        "import matplotlib.pyplot as plt\n",
                        "import seaborn as sns\n",
                        "import sys\n",
                        "import os\n",
                        "\n",
                        "# Add AI PM Toolkit to path\n",
                        "sys.path.append('../shared')\n",
                        "from market_research import research_company_data\n",
                        "\n",
                        "# Configure plotting\n",
                        "plt.style.use('seaborn-v0_8')\n",
                        "sns.set_palette('husl')\n",
                        "\n",
                        "print('✅ AI PM Market Research Environment Ready!')"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 📈 Company Analysis\n",
                        "\n",
                        "Research a specific company using real financial data:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Configure company research\n",
                        "TICKER = 'AAPL'  # Change this to any public company ticker\n",
                        "COMPANY_NAME = 'Apple Inc.'\n",
                        "\n",
                        "# Conduct research\n",
                        "result = research_company_data(\n",
                        "    ticker=TICKER,\n",
                        "    company_name=COMPANY_NAME,\n",
                        "    experience_type='learn_and_do',\n",
                        "    working_dir='../'\n",
                        ")\n",
                        "\n",
                        "if result['success']:\n",
                        "    print(f'✅ Research completed for {COMPANY_NAME}')\n",
                        "    \n",
                        "    # Extract data for analysis\n",
                        "    company_info = result['results']['company_info']\n",
                        "    financials = result['results']['financials']\n",
                        "    \n",
                        "    # Display key metrics\n",
                        "    print(f'Market Cap: ${financials.get(\"market_cap\", 0):,}')\n",
                        "    print(f'P/E Ratio: {financials.get(\"pe_ratio\", \"N/A\")}')\n",
                        "    print(f'Industry: {company_info.get(\"industry\", \"Unknown\")}')\n",
                        "else:\n",
                        "    print(f'❌ Research failed: {result.get(\"error\")}')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    def _get_user_data_template(self) -> Dict:
        """Generate user data analysis template"""
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 👥 User Data Analysis for Product Managers\n",
                        "\n",
                        "Analyze user behavior and engagement metrics to inform product decisions.\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Import libraries\n",
                        "import pandas as pd\n",
                        "import matplotlib.pyplot as plt\n",
                        "import seaborn as sns\n",
                        "import sys\n",
                        "\n",
                        "# Add AI PM Toolkit\n",
                        "sys.path.append('../shared')\n",
                        "from data_generator import generate_sample_data\n",
                        "\n",
                        "print('👥 User Data Analysis Environment Ready!')"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Generate Sample User Data\n",
                        "\n",
                        "Create realistic user data for analysis:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Generate user personas\n",
                        "result = generate_sample_data(\n",
                        "    experience_type='learn_and_do',\n",
                        "    working_dir='../',\n",
                        "    count=100,\n",
                        "    persona_type='b2c_consumer'\n",
                        ")\n",
                        "\n",
                        "if result['success']:\n",
                        "    print(f'✅ Generated {result[\"personas_generated\"]} user personas')\n",
                        "    \n",
                        "    # Load the generated data\n",
                        "    personas_df = pd.DataFrame(result['personas'])\n",
                        "    print(f'📊 Dataset shape: {personas_df.shape}')\n",
                        "    print('\\nSample data:')\n",
                        "    print(personas_df.head())\n",
                        "else:\n",
                        "    print(f'❌ Data generation failed: {result.get(\"error\")}')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python", 
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    def _get_synthetic_data_template(self) -> Dict:
        """Generate synthetic data experimentation template"""
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🧪 Synthetic Data Experiments for PMs\n",
                        "\n",
                        "Test product hypotheses with synthetic data before building features.\n"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    def _get_competitive_analysis_template(self) -> Dict:
        """Generate competitive analysis template"""
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🥊 Competitive Analysis Dashboard\n",
                        "\n",
                        "Compare multiple companies and analyze competitive landscapes.\n"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    def _setup_jupyter_config(self, config: JupyterConfig):
        """Set up Jupyter configuration for PM use"""
        # This could include custom extensions, themes, etc.
        pass
    
    def start_jupyter_lab(self, config: JupyterConfig) -> Dict[str, Any]:
        """Start Jupyter Lab server"""
        
        # Set up environment first
        setup_result = self.setup_jupyter_environment(config)
        
        # Build jupyter lab command
        notebook_dir = self.working_dir / config.notebook_dir
        
        cmd = [
            'jupyter-lab',
            f'--port={config.port}',
            f'--notebook-dir={notebook_dir}',
            '--no-browser' if not config.auto_open_browser else '',
        ]
        
        # Remove empty strings
        cmd = [arg for arg in cmd if arg]
        
        if not config.allow_external_access:
            cmd.extend(['--ip=127.0.0.1'])
        
        try:
            # Start Jupyter Lab
            print(f"🚀 Starting Jupyter Lab on port {config.port}...")
            print(f"📁 Notebook directory: {notebook_dir}")
            
            self.jupyter_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Give it time to start
            time.sleep(3)
            
            # Check if process is running
            if self.jupyter_process.poll() is None:
                url = f"http://localhost:{config.port}"
                
                # Open browser if configured
                if config.auto_open_browser:
                    try:
                        webbrowser.open(url)
                    except:
                        pass
                
                return {
                    "success": True,
                    "url": url,
                    "port": config.port,
                    "notebook_dir": str(notebook_dir),
                    "pid": self.jupyter_process.pid,
                    "setup_info": setup_result
                }
            else:
                # Process failed to start
                output = self.jupyter_process.stdout.read() if self.jupyter_process.stdout else ""
                return {
                    "success": False,
                    "error": f"Jupyter Lab failed to start: {output}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start Jupyter Lab: {str(e)}"
            }
    
    def stop_jupyter_lab(self) -> bool:
        """Stop running Jupyter Lab server"""
        if self.jupyter_process:
            try:
                self.jupyter_process.terminate()
                self.jupyter_process.wait(timeout=10)
                return True
            except:
                try:
                    self.jupyter_process.kill()
                    return True
                except:
                    return False
        return True
    
    def get_jupyter_status(self) -> Dict[str, Any]:
        """Get status of Jupyter Lab server"""
        if not self.jupyter_process:
            return {"running": False}
        
        poll_result = self.jupyter_process.poll()
        
        return {
            "running": poll_result is None,
            "pid": self.jupyter_process.pid if poll_result is None else None,
            "return_code": poll_result
        }
    
    def list_notebooks(self) -> List[Dict[str, Any]]:
        """List available notebooks"""
        if not self.config:
            return []
        
        notebook_dir = self.working_dir / self.config.notebook_dir
        notebooks = []
        
        for notebook_file in notebook_dir.rglob("*.ipynb"):
            try:
                stat = notebook_file.stat()
                notebooks.append({
                    "name": notebook_file.name,
                    "path": str(notebook_file.relative_to(notebook_dir)),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "is_template": "template" in notebook_file.name.lower()
                })
            except:
                continue
        
        return sorted(notebooks, key=lambda x: x["modified"], reverse=True)

def start_jupyter_session(port: int = 8888, experience_type: str = "just_do_it", 
                         working_dir: str = ".") -> Dict[str, Any]:
    """Main entry point for Jupyter Lab integration"""
    
    manager = JupyterLabManager(working_dir)
    
    # Check availability first
    availability = manager.check_jupyter_availability()
    
    if not availability["jupyterlab"]:
        return {
            "success": False,
            "error": "Jupyter Lab not available. Install with: pip install jupyterlab",
            "availability": availability
        }
    
    # Configure based on experience type
    config = JupyterConfig(
        port=port,
        working_dir=working_dir,
        auto_open_browser=experience_type != "cli_deep_dive",
        enable_extensions=experience_type in ["learn_and_do", "cli_deep_dive"]
    )
    
    manager.config = config
    
    # Start Jupyter Lab
    result = manager.start_jupyter_lab(config)
    
    if result["success"]:
        result["manager"] = manager
        result["availability"] = availability
    
    return result

# CLI entry point for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - Jupyter Lab Integration")
    parser.add_argument("--port", type=int, default=8888, help="Jupyter Lab port")
    parser.add_argument("--experience", choices=["just_do_it", "learn_and_do", "cli_deep_dive"],
                       default="just_do_it", help="Experience type")
    parser.add_argument("--dir", default=".", help="Working directory")
    parser.add_argument("--check", action="store_true", help="Check availability only")
    
    args = parser.parse_args()
    
    try:
        if args.check:
            # Just check availability
            manager = JupyterLabManager(args.dir)
            availability = manager.check_jupyter_availability()
            
            print("📊 Jupyter Lab Availability Check:")
            for component, available in availability.items():
                if component != "version_info":
                    status = "✅" if available else "❌"
                    print(f"   {status} {component}")
            
            if availability["version_info"]:
                print("\n📋 Version Info:")
                for component, version in availability["version_info"].items():
                    print(f"   {component}: {version}")
        else:
            # Start Jupyter Lab
            result = start_jupyter_session(
                port=args.port,
                experience_type=args.experience,
                working_dir=args.dir
            )
            
            if result["success"]:
                print(f"🚀 Jupyter Lab started successfully!")
                print(f"🌐 URL: {result['url']}")
                print(f"📁 Notebook directory: {result['notebook_dir']}")
                print(f"📝 Templates: {result['setup_info']['templates_created']} categories created")
                print("\n⚠️  Press Ctrl+C to stop Jupyter Lab")
                
                # Keep running
                try:
                    manager = result["manager"]
                    while True:
                        status = manager.get_jupyter_status()
                        if not status["running"]:
                            print("\n🛑 Jupyter Lab stopped")
                            break
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping Jupyter Lab...")
                    if "manager" in result:
                        result["manager"].stop_jupyter_lab()
                    print("✅ Jupyter Lab stopped")
            else:
                print(f"❌ Failed to start Jupyter Lab: {result['error']}")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)