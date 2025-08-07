#!/usr/bin/env python3
"""
AI PM Toolkit - Simple Web Dashboard
Phase 1: Foundation with clean, minimal Flask server
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from dataclasses import asdict
from pathlib import Path
from flask import Flask, render_template, jsonify, request, make_response, g

# Add shared modules to path
sys.path.append(str(Path(__file__).parent.parent / 'shared'))
from auth_manager import AuthenticationManager, require_auth, require_role

# Initialize Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize authentication manager
auth_manager = AuthenticationManager(str(Path(__file__).parent.parent))

# Load toolkit configuration
TOOLKIT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = TOOLKIT_ROOT / "toolkit.json"

def load_config():
    """Load toolkit configuration"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {"tools": [], "experiences": {}}

config = load_config()

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login endpoint"""
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Get client info
        ip_address = request.remote_addr or ''
        user_agent = request.headers.get('User-Agent', '')
        
        # Authenticate user
        result = auth_manager.authenticate_user(email, password, ip_address, user_agent)
        
        if result['success']:
            # Set session cookie
            response = make_response(jsonify(result))
            response.set_cookie('aipm_session', result['session_id'], 
                              httponly=True, secure=False, samesite='Lax')
            return response
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """User logout endpoint"""
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_id:
            session_id = request.cookies.get('aipm_session')
        
        if session_id:
            auth_manager.logout_user(session_id)
        
        # Clear session cookie
        response = make_response(jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }))
        response.set_cookie('aipm_session', '', expires=0)
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/status')
def api_auth_status():
    """Check authentication status"""
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_id:
            session_id = request.cookies.get('aipm_session')
        
        if not session_id:
            return jsonify({
                'authenticated': False,
                'guest_mode_available': auth_manager.config.get('enable_guest_mode', True)
            })
        
        validation = auth_manager.validate_session(session_id)
        
        if validation['valid']:
            return jsonify({
                'authenticated': True,
                'user': validation['user'],
                'session': validation['session']
            })
        else:
            return jsonify({
                'authenticated': False,
                'error': validation['error'],
                'guest_mode_available': auth_manager.config.get('enable_guest_mode', True)
            })
            
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'error': str(e),
            'guest_mode_available': True
        })

@app.route('/api/auth/guest', methods=['POST'])
def api_guest_login():
    """Create guest session"""
    try:
        ip_address = request.remote_addr or ''
        user_agent = request.headers.get('User-Agent', '')
        
        result = auth_manager.guest_session(ip_address, user_agent)
        
        if result['success']:
            response = make_response(jsonify(result))
            response.set_cookie('aipm_session', result['session_id'], 
                              httponly=True, secure=False, samesite='Lax')
            return response
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """User registration endpoint"""
    try:
        if not auth_manager.config.get('allow_registration', True):
            return jsonify({
                'success': False,
                'error': 'Registration is currently disabled'
            }), 403
        
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        password = data.get('password', '')
        
        if not all([email, name, password]):
            return jsonify({
                'success': False,
                'error': 'Email, name, and password are required'
            }), 400
        
        result = auth_manager.create_user(email, name, password)
        return jsonify(result), 201 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/')
def dashboard():
    """Main dashboard page"""
    # Check if user is authenticated
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not session_id:
        session_id = request.cookies.get('aipm_session')
    
    user_info = None
    if session_id:
        validation = auth_manager.validate_session(session_id)
        if validation['valid']:
            user_info = validation['user']
        else:
            # Invalid session, redirect to login
            return render_template('login.html')
    else:
        # No session, redirect to login
        return render_template('login.html')
    
    return render_template('dashboard.html', 
                         toolkit=config,
                         tools=config.get('tools', []),
                         experiences=config.get('experiences', {}),
                         user=user_info)

@app.route('/api/tools')
def api_tools():
    """API endpoint for tools list"""
    return jsonify(config.get('tools', []))

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify({
        "status": "running",
        "version": config.get('version', '1.0.0'),
        "tools_count": len(config.get('tools', [])),
        "interfaces": ["web", "cli"]
    })

@app.route('/tool/<tool_id>')
def tool_page(tool_id):
    """Individual tool page"""
    tool = next((t for t in config.get('tools', []) if t['id'] == tool_id), None)
    if not tool:
        return "Tool not found", 404
    
    return render_template('tool.html', tool=tool)

@app.route('/api/generate-data', methods=['POST'])
@require_auth
def api_generate_data():
    """API endpoint for data generation"""
    try:
        # Import the shared data generator
        import sys
        import os
        shared_path = os.path.join(os.path.dirname(__file__), '..', 'shared')
        if shared_path not in sys.path:
            sys.path.append(shared_path)
            
        from data_generator import generate_sample_data
        
        # Get parameters from request
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
        experience_type = data.get('experience_type', 'just_do_it')
        working_dir = data.get('working_dir', '.')
        count = data.get('count', 10)
        persona_type = data.get('persona_type', 'b2b_saas')
        
        # Validate count parameter
        try:
            count = int(count)
            if count <= 0 or count > 1000:
                return jsonify({"success": False, "error": "Count must be between 1 and 1000"}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Count must be a valid number"}), 400
        
        # Generate data
        result = generate_sample_data(
            experience_type=experience_type,
            working_dir=working_dir,
            count=count,
            persona_type=persona_type
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/market-research', methods=['POST'])
@require_auth  
def api_market_research():
    """API endpoint for market research"""
    try:
        # Import the shared market research engine
        import sys
        import os
        shared_path = os.path.join(os.path.dirname(__file__), '..', 'shared')
        if shared_path not in sys.path:
            sys.path.append(shared_path)
            
        from market_research import research_company_data, research_market_data
        
        # Get parameters from request
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
        research_type = data.get('type', 'company')
        experience_type = data.get('experience_type', 'just_do_it')
        working_dir = data.get('working_dir', '.')
        
        if research_type == 'company':
            # Company research
            company_name = data.get('company_name')
            ticker = data.get('ticker')
            
            if not company_name and not ticker:
                return jsonify({
                    "success": False,
                    "error": "Please provide either company_name or ticker"
                }), 400
            
            result = research_company_data(
                ticker=ticker,
                company_name=company_name,
                experience_type=experience_type,
                working_dir=working_dir
            )
        else:
            # Market research
            industry = data.get('industry', 'technology')
            market_type = data.get('market_type', 'b2b_saas')
            
            result = research_market_data(
                industry=industry,
                market_type=market_type,
                experience_type=experience_type,
                working_dir=working_dir
            )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ai-chat', methods=['POST'])
@require_auth
def api_ai_chat():
    """API endpoint for AI chat"""
    try:
        # Import the shared AI chat engine
        import sys
        import os
        shared_path = os.path.join(os.path.dirname(__file__), '..', 'shared')
        if shared_path not in sys.path:
            sys.path.append(shared_path)
        
        from ai_chat import start_ai_chat, AIChat, ChatConfig
        
        # Get parameters from request
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
        action = data.get('action', 'start')
        
        if action == 'status':
            # Check available models
            chat_engine = AIChat('.')
            available_models = chat_engine.available_models
            
            # Extract model names that are available
            model_list = []
            if available_models.get('gpt-oss-20b'):
                model_list.append('gpt-oss-20b')
            if available_models.get('qwen2.5'):
                model_list.append('qwen2.5')
            if available_models.get('deepseek-r1'):
                model_list.append('deepseek-r1')
            if available_models.get('llama3.2'):
                model_list.append('llama3.2')
            if available_models.get('llama3.2-3b'):
                model_list.append('llama3.2-3b')
            
            return jsonify({
                "success": True,
                "status": "available",
                "models": model_list,
                "ollama_available": available_models.get('ollama', False)
            })
        
        elif action == 'start':
            chat_mode = data.get('chat_mode', 'pm_assistant')
            model = data.get('model', 'local')
            experience_type = data.get('experience_type', 'just_do_it')
            working_dir = data.get('working_dir', '.')
            
            result = start_ai_chat(
                chat_mode=chat_mode,
                model=model,
                experience_type=experience_type,
                working_dir=working_dir
            )
            
            if result.get("success"):
                return jsonify({
                    "success": True,
                    "session_info": result["session_info"],
                    "config": result["config"]
                })
            else:
                return jsonify({
                    "success": False,
                    "error": result.get("error", "Failed to start chat session")
                }), 500
            
        elif action == 'send':
            # This would require session management - simplified for Phase 3
            message = data.get('message', '')
            if not message.strip():
                return jsonify({"success": False, "error": "Empty message"}), 400
                
            chat_mode = data.get('chat_mode', 'pm_assistant')
            
            # Create temporary chat instance for demo
            chat_engine = AIChat('.')
            config = ChatConfig(chat_mode=chat_mode)
            chat_engine.start_chat_session(config)
            
            response = chat_engine.send_message(message, config)
            
            return jsonify({
                "success": True,
                "response": response["response"],
                "tokens_used": response["tokens_used"]
            })
        
        elif action == 'save_conversation':
            # Save current conversation
            session_id = data.get('session_id', 'unknown')
            messages = data.get('messages', [])
            
            # Create temporary chat engine with conversation history
            chat_engine = AIChat('.')
            
            # Reconstruct conversation history
            for msg_data in messages:
                from ai_chat import ChatMessage
                message = ChatMessage(
                    role=msg_data.get('role', 'user'),
                    content=msg_data.get('content', ''),
                    timestamp=msg_data.get('timestamp', datetime.now().isoformat()),
                    tokens=msg_data.get('tokens')
                )
                chat_engine.conversation_history.append(message)
            
            # Save conversation
            filename = chat_engine.save_conversation(session_id=session_id)
            
            return jsonify({
                "success": True,
                "filename": os.path.basename(filename),
                "full_path": filename
            })
            
        elif action == 'list_conversations':
            # List saved conversations
            chat_engine = AIChat('.')
            conversations = chat_engine.list_saved_conversations()
            
            return jsonify({
                "success": True,
                "conversations": conversations
            })
            
        elif action == 'load_conversation':
            # Load a specific conversation
            filename = data.get('filename')
            if not filename:
                return jsonify({"success": False, "error": "Filename required"}), 400
                
            chat_engine = AIChat('.')
            if chat_engine.load_conversation(filename):
                return jsonify({
                    "success": True,
                    "messages": [asdict(msg) for msg in chat_engine.conversation_history],
                    "summary": chat_engine.get_conversation_summary()
                })
            else:
                return jsonify({"success": False, "error": "Failed to load conversation"}), 500
        
        return jsonify({"success": False, "error": f"Invalid action: {action}"}), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/workflow-status')
def api_workflow_status():
    """API endpoint for workflow status checking"""
    try:
        import subprocess
        import socket
        
        status = {
            "n8n": False,
            "docker": False,
            "network": False
        }
        
        # Check if Docker is available
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            status["docker"] = result.returncode == 0
        except:
            status["docker"] = False
        
        # Check if n8n is running on port 5678
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 5678))
            status["n8n"] = result == 0
            sock.close()
        except:
            status["n8n"] = False
        
        # Network is ready if we can perform basic checks
        status["network"] = True
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            "n8n": False,
            "docker": False,
            "network": False,
            "error": str(e)
        }), 500

@app.route('/api/workflow-control', methods=['POST'])
@require_auth
def api_workflow_control():
    """API endpoint for workflow control (start/stop/restart)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
        action = data.get('action', 'start')
        service = data.get('service', 'n8n')
        
        # Validate action parameter
        valid_actions = ['start', 'stop', 'restart', 'status', 'cleanup']
        if action not in valid_actions:
            return jsonify({
                "success": False,
                "error": f"Invalid action. Must be one of: {', '.join(valid_actions)}"
            }), 400
        
        # Path to orchestration script
        script_path = Path(__file__).parent.parent / "workflow-tools" / "orchestrate-workflows.sh"
        
        if not script_path.exists():
            return jsonify({
                "success": False,
                "error": "Orchestration script not found. Please ensure workflow-tools directory exists."
            }), 404
        
        # Build command
        cmd = [str(script_path), action]
        if service and service != 'all':
            cmd.append(service)
        
        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        return jsonify({
            "success": result.returncode == 0,
            "command": ' '.join(cmd),
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "return_code": result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Command timed out after 60 seconds"
        }), 408
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/workflow-setup', methods=['POST'])
def api_workflow_setup():
    """API endpoint for guided workflow setup"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
        port = data.get('port', 5678)
        environment = data.get('environment', 'development')
        persistence = data.get('persistence', True)
        usecases = data.get('usecases', [])
        
        # Validate port
        try:
            port = int(port)
            if port < 3000 or port > 9999:
                return jsonify({"success": False, "error": "Port must be between 3000 and 9999"}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Port must be a valid number"}), 400
        
        # For Phase 3, we'll use the existing orchestration script
        # In a full implementation, this would configure n8n with custom settings
        
        script_path = Path(__file__).parent.parent / "workflow-tools" / "orchestrate-workflows.sh"
        
        if not script_path.exists():
            return jsonify({
                "success": False,
                "error": "Orchestration script not found"
            }), 404
        
        # Start n8n with default configuration
        result = subprocess.run([str(script_path), "start", "n8n"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return jsonify({
                "success": True,
                "message": "n8n workflow system configured and started",
                "config": {
                    "port": port,
                    "environment": environment,
                    "persistence": persistence,
                    "usecases": usecases
                },
                "url": f"http://localhost:{port}",
                "output": result.stdout
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to start n8n",
                "output": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/jupyter', methods=['POST'])
@require_auth
def api_jupyter():
    """API endpoint for Jupyter Lab integration"""
    try:
        data = request.get_json() or {}
        action = data.get('action', 'status')
        
        if action == 'start':
            port = data.get('port', 8888)
            experience_type = data.get('experience_type', 'learn_and_do')
            
            import sys
            sys.path.append(str(TOOLKIT_ROOT / 'shared'))
            from jupyter_integration import start_jupyter_session
            
            result = start_jupyter_session(
                port=port,
                experience_type=experience_type,
                working_dir=str(TOOLKIT_ROOT)
            )
            
            return jsonify(result)
        
        elif action == 'check':
            import sys
            sys.path.append(str(TOOLKIT_ROOT / 'shared'))
            from jupyter_integration import JupyterLabManager
            
            manager = JupyterLabManager(str(TOOLKIT_ROOT))
            availability = manager.check_jupyter_availability()
            
            return jsonify({
                'success': True,
                'availability': availability
            })
        
        elif action == 'notebooks':
            import sys
            sys.path.append(str(TOOLKIT_ROOT / 'shared'))
            from jupyter_integration import JupyterLabManager
            
            manager = JupyterLabManager(str(TOOLKIT_ROOT))
            notebooks = manager.list_notebooks()
            
            return jsonify({
                'success': True,
                'notebooks': notebooks
            })
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown action: {action}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/langflow', methods=['POST'])
@require_auth
def api_langflow():
    """API endpoint for Langflow integration"""
    try:
        data = request.get_json() or {}
        action = data.get('action', 'status')
        
        if action == 'start':
            # Start Langflow using orchestration script
            script_path = TOOLKIT_ROOT / "workflow-tools" / "orchestrate-workflows.sh"
            result = subprocess.run([str(script_path), "langflow"], 
                                  capture_output=True, text=True, timeout=120)
            
            return jsonify({
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None,
                'url': 'http://localhost:7860' if result.returncode == 0 else None
            })
        
        elif action == 'status':
            # Check if Langflow is running
            import socket
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('localhost', 7860))
                is_running = result == 0
                sock.close()
                
                return jsonify({
                    'success': True,
                    'running': is_running,
                    'url': 'http://localhost:7860' if is_running else None,
                    'port': 7860
                })
            except:
                return jsonify({
                    'success': True,
                    'running': False,
                    'url': None,
                    'port': 7860
                })
        
        elif action == 'stop':
            # Stop Langflow
            try:
                result = subprocess.run(['docker', 'stop', 'aipm-langflow'], 
                                      capture_output=True, text=True, timeout=30)
                subprocess.run(['docker', 'rm', 'aipm-langflow'], 
                             capture_output=True, text=True, timeout=10)
                
                return jsonify({
                    'success': True,
                    'message': 'Langflow stopped successfully'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        elif action == 'workflows':
            # List available workflows (placeholder for now)
            return jsonify({
                'success': True,
                'workflows': [
                    {
                        'name': 'PM Market Research',
                        'description': 'Automated market research using AI and live data',
                        'category': 'Research'
                    },
                    {
                        'name': 'Competitive Analysis',
                        'description': 'Multi-company analysis with financial data',
                        'category': 'Analysis'
                    },
                    {
                        'name': 'AI Chat Assistant',
                        'description': 'PM-focused conversational AI workflow',
                        'category': 'Assistant'
                    }
                ]
            })
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown action: {action}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/cli-bridge')
def cli_bridge():
    """Bridge page to CLI experience"""
    return render_template('cli-bridge.html')

if __name__ == '__main__':
    print("🌐 AI PM Toolkit - Web Dashboard")
    print("=" * 40)
    print(f"📁 Config: {CONFIG_PATH}")
    print(f"🔧 Tools loaded: {len(config.get('tools', []))}")
    print(f"🚀 Starting server at http://localhost:3000")
    print()
    
    app.run(host='localhost', port=3000, debug=True)