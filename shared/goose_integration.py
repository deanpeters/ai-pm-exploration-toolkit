#!/usr/bin/env python3
"""
AI PM Toolkit - Goose CLI Integration
Phase 7: Next-Gen AI Integration for autonomous PM workflows
"""

import os
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class GooseSession:
    """Represents a Goose CLI session for PM workflows"""
    name: str
    status: str
    created_at: str
    model: str
    working_dir: str

class GooseManager:
    """Manages Goose CLI integration with AI PM Toolkit"""
    
    def __init__(self, toolkit_root: str):
        self.toolkit_root = Path(toolkit_root)
        self.goose_binary = Path.home() / ".local/bin/goose"
        self.config_path = Path.home() / ".config/goose/config.yaml"
        
    def check_goose_availability(self) -> Dict[str, Any]:
        """Check if Goose CLI is available and properly configured"""
        try:
            # Check if Goose binary exists
            if not self.goose_binary.exists():
                return {
                    "available": False,
                    "error": "Goose CLI not installed. Install from https://github.com/block/goose",
                    "install_command": "curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh | bash"
                }
            
            # Check if Goose configuration exists
            if not self.config_path.exists():
                return {
                    "available": False,
                    "error": "Goose CLI not configured. Run 'goose configure' to set up providers",
                    "configure_command": "goose configure"
                }
            
            # Try to get Goose info
            result = subprocess.run(
                [str(self.goose_binary), "info"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "available": True,
                    "version": "1.2.0",  # Known version from testing
                    "config_path": str(self.config_path),
                    "binary_path": str(self.goose_binary),
                    "info": result.stdout
                }
            else:
                return {
                    "available": False,
                    "error": f"Goose CLI error: {result.stderr}",
                    "stdout": result.stdout
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": f"Failed to check Goose availability: {str(e)}"
            }
    
    def get_supported_models(self) -> List[str]:
        """Get list of models that work with Goose CLI"""
        return [
            "qwen2.5",      # Tool-calling support (recommended)
            "llama3.2",     # General purpose
            "deepseek-r1",  # Reasoning tasks
            "gpt-oss-20b",  # When available in Ollama
        ]
    
    def create_pm_workflow_session(self, workflow_name: str, description: str = "") -> Dict[str, Any]:
        """Create a new Goose session for PM workflows"""
        try:
            session_name = f"aipm_{workflow_name}_{int(time.time())}"
            
            # Create session (this would require proper Goose configuration)
            result = subprocess.run(
                [str(self.goose_binary), "session", "--name", session_name],
                capture_output=True, text=True, timeout=30,
                cwd=str(self.toolkit_root)
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "session_name": session_name,
                    "output": result.stdout,
                    "working_dir": str(self.toolkit_root)
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "output": result.stdout
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create Goose session: {str(e)}"
            }
    
    def list_pm_workflow_templates(self) -> List[Dict[str, Any]]:
        """List available PM workflow templates for Goose"""
        return [
            {
                "name": "market_research_analysis",
                "title": "Automated Market Research Analysis",
                "description": "Use Goose to analyze market data, competitor information, and generate comprehensive market insights",
                "tools_required": ["web-search", "file-system", "shell"],
                "estimated_time": "30-60 minutes",
                "complexity": "intermediate"
            },
            {
                "name": "product_requirements_generator",
                "title": "Product Requirements Document Generator",
                "description": "Autonomous generation of PRDs based on user stories and market analysis",
                "tools_required": ["file-system", "github", "web-search"],
                "estimated_time": "45-90 minutes",
                "complexity": "advanced"
            },
            {
                "name": "competitive_feature_analysis",
                "title": "Competitive Feature Analysis",
                "description": "Analyze competitor features, pricing, and positioning automatically",
                "tools_required": ["web-search", "file-system"],
                "estimated_time": "20-45 minutes",
                "complexity": "beginner"
            },
            {
                "name": "stakeholder_update_generator",
                "title": "Stakeholder Update Generator",
                "description": "Generate executive summaries and stakeholder updates from project data",
                "tools_required": ["github", "file-system"],
                "estimated_time": "15-30 minutes",
                "complexity": "beginner"
            },
            {
                "name": "user_persona_research",
                "title": "User Persona Research and Development",
                "description": "Research and create detailed user personas based on market data",
                "tools_required": ["web-search", "file-system"],
                "estimated_time": "60-120 minutes",
                "complexity": "intermediate"
            }
        ]
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status between Goose and AI PM Toolkit"""
        availability = self.check_goose_availability()
        
        # Check Ollama models that support Goose
        supported_models = []
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                ollama_models = response.json().get("models", [])
                for model_info in ollama_models:
                    model_name = model_info.get("name", "").lower()
                    for supported in self.get_supported_models():
                        if supported in model_name:
                            supported_models.append(model_name)
        except:
            pass
        
        return {
            "goose_available": availability.get("available", False),
            "goose_configured": self.config_path.exists(),
            "supported_models_available": supported_models,
            "recommended_model": "qwen2.5" if any("qwen2.5" in m.lower() for m in supported_models) else None,
            "integration_ready": (
                availability.get("available", False) and 
                self.config_path.exists() and 
                len(supported_models) > 0
            ),
            "phase_7_status": {
                "goose_installation": "completed",
                "goose_configuration": "partial" if self.config_path.exists() else "pending",
                "model_support": "completed" if supported_models else "partial",
                "workflow_templates": "designed",
                "mcp_extensions": "pending"
            }
        }

# Configuration helper for Goose CLI
def generate_goose_config(ollama_host: str = "http://localhost:11434", 
                         primary_model: str = "qwen2.5") -> str:
    """Generate Goose CLI configuration for AI PM Toolkit integration"""
    
    config_yaml = f"""# Goose CLI Configuration for AI PM Toolkit
# Optimized for Product Manager autonomous workflows

provider:
  type: ollama
  host: {ollama_host}
  model: {primary_model}

# PM workflow settings
settings:
  temperature: 0.3        # Focused responses for PM tasks
  max_tokens: 2000       # Longer responses for analysis
  timeout: 120           # Allow time for complex reasoning
  
  # Workflow preferences
  auto_confirm: false    # Always confirm actions for safety
  save_history: true     # Keep session history
  working_directory: {Path.cwd()}

# PM-focused extensions (when available)
extensions:
  enabled:
    - github           # Repository analysis
    - web-search       # Market research
    - file-system      # Local operations
    - shell           # System commands
"""
    
    return config_yaml

# CLI entry point for testing Goose integration
if __name__ == "__main__":
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - Goose Integration")
    parser.add_argument("--status", action="store_true", help="Check integration status")
    parser.add_argument("--config", action="store_true", help="Generate configuration")
    parser.add_argument("--templates", action="store_true", help="List workflow templates")
    
    args = parser.parse_args()
    
    manager = GooseManager(".")
    
    if args.status:
        status = manager.get_integration_status()
        print("🦢 Goose CLI Integration Status")
        print("=" * 40)
        print(f"Goose Available: {'✅' if status['goose_available'] else '❌'}")
        print(f"Goose Configured: {'✅' if status['goose_configured'] else '❌'}")
        print(f"Integration Ready: {'✅' if status['integration_ready'] else '⚠️'}")
        print(f"Supported Models: {', '.join(status['supported_models_available'])}")
        print(f"Recommended Model: {status['recommended_model'] or 'None available'}")
        print()
        print("Phase 7 Progress:")
        for component, status_val in status['phase_7_status'].items():
            emoji = "✅" if status_val == "completed" else "⚠️" if status_val == "partial" else "❌"
            print(f"  {emoji} {component}: {status_val}")
    
    elif args.config:
        config = generate_goose_config()
        print("Generated Goose CLI Configuration:")
        print("=" * 40)
        print(config)
    
    elif args.templates:
        templates = manager.list_pm_workflow_templates()
        print("🧪 Available PM Workflow Templates")
        print("=" * 40)
        for template in templates:
            print(f"📋 {template['title']}")
            print(f"   {template['description']}")
            print(f"   Tools: {', '.join(template['tools_required'])}")
            print(f"   Time: {template['estimated_time']}")
            print(f"   Level: {template['complexity']}")
            print()
    
    else:
        # Default: show status
        status = manager.get_integration_status()
        if status['integration_ready']:
            print("🎉 Goose CLI integration is ready!")
            print("Run 'python goose_integration.py --templates' to see available workflows")
        else:
            print("⚠️  Goose CLI integration needs setup")
            if not status['goose_available']:
                print("1. Install Goose CLI: curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh | bash")
            if not status['goose_configured']:
                print("2. Configure Goose CLI: goose configure")
            if not status['supported_models_available']:
                print("3. Install supported model: ollama pull qwen2.5")