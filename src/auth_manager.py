#!/usr/bin/env python3
"""
AI PM Toolkit - Authentication and Session Management
Production-ready authentication system for PM toolkit access
"""

import hashlib
import json
import os
import secrets
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import uuid

@dataclass
class User:
    """User account representation"""
    user_id: str
    email: str
    name: str
    role: str = "pm"  # pm, admin, viewer
    created_at: str = ""
    last_login: str = ""
    is_active: bool = True
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.preferences is None:
            self.preferences = {
                "theme": "light",
                "default_experience": "learn_and_do",
                "favorite_tools": [],
                "dashboard_layout": "default"
            }

@dataclass
class Session:
    """Active user session"""
    session_id: str
    user_id: str
    created_at: str
    expires_at: str
    last_active: str
    ip_address: str = ""
    user_agent: str = ""
    is_active: bool = True
    
class AuthenticationManager:
    """Production-ready authentication and session management"""
    
    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.auth_dir = self.working_dir / "auth"
        self.auth_dir.mkdir(exist_ok=True)
        
        # File paths
        self.users_file = self.auth_dir / "users.json"
        self.sessions_file = self.auth_dir / "sessions.json"
        self.config_file = self.auth_dir / "auth_config.json"
        
        # Load configuration
        self.config = self._load_auth_config()
        
        # Initialize default admin user if no users exist
        self._initialize_default_users()
    
    def _load_auth_config(self) -> Dict[str, Any]:
        """Load authentication configuration"""
        default_config = {
            "session_timeout_hours": 24,
            "max_sessions_per_user": 5,
            "require_strong_passwords": False,  # Disabled for PM toolkit simplicity
            "allow_registration": True,
            "default_role": "pm",
            "enable_guest_mode": True,
            "secret_key": secrets.token_urlsafe(32)
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                # Create default config
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
                
        except Exception as e:
            print(f"Error loading auth config: {e}")
            return default_config
    
    def _initialize_default_users(self):
        """Create default admin user if no users exist"""
        users = self._load_users()
        
        if not users:
            # Create default PM user
            default_user = User(
                user_id="default_pm",
                email="pm@aipmtoolkit.local",
                name="Product Manager",
                role="pm"
            )
            
            # Simple default password (toolkit is for local development)
            password_hash = self._hash_password("aipm2025")
            
            users["default_pm"] = {
                **asdict(default_user),
                "password_hash": password_hash
            }
            
            self._save_users(users)
            print("🔐 Created default PM user: pm@aipmtoolkit.local / aipm2025")
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users from file"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
        return {}
    
    def _save_users(self, users: Dict[str, Any]):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _load_sessions(self) -> Dict[str, Any]:
        """Load sessions from file"""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
                    # Clean up expired sessions
                    return self._cleanup_expired_sessions(sessions)
        except Exception as e:
            print(f"Error loading sessions: {e}")
        return {}
    
    def _save_sessions(self, sessions: Dict[str, Any]):
        """Save sessions to file"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def _cleanup_expired_sessions(self, sessions: Dict[str, Any]) -> Dict[str, Any]:
        """Remove expired sessions"""
        now = datetime.now()
        active_sessions = {}
        
        for session_id, session_data in sessions.items():
            try:
                expires_at = datetime.fromisoformat(session_data.get('expires_at', ''))
                if expires_at > now and session_data.get('is_active', True):
                    active_sessions[session_id] = session_data
            except:
                continue  # Skip malformed sessions
        
        return active_sessions
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt (simple but secure for local toolkit)"""
        salt = self.config['secret_key']
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _generate_session_id(self) -> str:
        """Generate secure session ID"""
        return secrets.token_urlsafe(32)
    
    def create_user(self, email: str, name: str, password: str, 
                   role: str = "pm") -> Dict[str, Any]:
        """Create a new user account"""
        users = self._load_users()
        
        # Check if user already exists
        for user_data in users.values():
            if user_data.get('email', '').lower() == email.lower():
                return {
                    'success': False,
                    'error': 'User with this email already exists'
                }
        
        # Create new user
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            email=email,
            name=name,
            role=role
        )
        
        password_hash = self._hash_password(password)
        
        users[user_id] = {
            **asdict(user),
            'password_hash': password_hash
        }
        
        self._save_users(users)
        
        return {
            'success': True,
            'user_id': user_id,
            'message': f'User {name} created successfully'
        }
    
    def authenticate_user(self, email: str, password: str, 
                         ip_address: str = "", user_agent: str = "") -> Dict[str, Any]:
        """Authenticate user and create session"""
        users = self._load_users()
        
        # Find user by email
        user_data = None
        for uid, data in users.items():
            if data.get('email', '').lower() == email.lower():
                user_data = data
                break
        
        if not user_data:
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        # Verify password
        password_hash = self._hash_password(password)
        if password_hash != user_data.get('password_hash'):
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        # Check if user is active
        if not user_data.get('is_active', True):
            return {
                'success': False,
                'error': 'User account is disabled'
            }
        
        # Create session
        session_id = self._generate_session_id()
        now = datetime.now()
        expires_at = now + timedelta(hours=self.config['session_timeout_hours'])
        
        session = Session(
            session_id=session_id,
            user_id=user_data['user_id'],
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            last_active=now.isoformat(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Save session
        sessions = self._load_sessions()
        sessions[session_id] = asdict(session)
        self._save_sessions(sessions)
        
        # Update user's last login
        user_data['last_login'] = now.isoformat()
        users[user_data['user_id']] = user_data
        self._save_users(users)
        
        return {
            'success': True,
            'session_id': session_id,
            'user': {
                'user_id': user_data['user_id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'role': user_data['role'],
                'preferences': user_data.get('preferences', {})
            },
            'expires_at': expires_at.isoformat()
        }
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate session and return user info"""
        if not session_id:
            return {'valid': False, 'error': 'No session ID provided'}
        
        sessions = self._load_sessions()
        session_data = sessions.get(session_id)
        
        if not session_data:
            return {'valid': False, 'error': 'Session not found'}
        
        # Check if session is expired
        try:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                # Remove expired session
                del sessions[session_id]
                self._save_sessions(sessions)
                return {'valid': False, 'error': 'Session expired'}
        except:
            return {'valid': False, 'error': 'Invalid session data'}
        
        # Update last active time
        session_data['last_active'] = datetime.now().isoformat()
        sessions[session_id] = session_data
        self._save_sessions(sessions)
        
        # Get user info
        users = self._load_users()
        user_data = users.get(session_data['user_id'])
        
        if not user_data or not user_data.get('is_active', True):
            return {'valid': False, 'error': 'User account not found or disabled'}
        
        return {
            'valid': True,
            'user': {
                'user_id': user_data['user_id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'role': user_data['role'],
                'preferences': user_data.get('preferences', {})
            },
            'session': {
                'session_id': session_id,
                'created_at': session_data['created_at'],
                'expires_at': session_data['expires_at'],
                'last_active': session_data['last_active']
            }
        }
    
    def logout_user(self, session_id: str) -> Dict[str, Any]:
        """Logout user by invalidating session"""
        sessions = self._load_sessions()
        
        if session_id in sessions:
            del sessions[session_id]
            self._save_sessions(sessions)
            return {'success': True, 'message': 'Logged out successfully'}
        
        return {'success': False, 'error': 'Session not found'}
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        sessions = self._load_sessions()
        user_sessions = []
        
        for session_id, session_data in sessions.items():
            if session_data.get('user_id') == user_id:
                user_sessions.append({
                    'session_id': session_id,
                    'created_at': session_data.get('created_at'),
                    'last_active': session_data.get('last_active'),
                    'ip_address': session_data.get('ip_address', ''),
                    'user_agent': session_data.get('user_agent', '')
                })
        
        return sorted(user_sessions, key=lambda x: x['last_active'], reverse=True)
    
    def guest_session(self, ip_address: str = "", user_agent: str = "") -> Dict[str, Any]:
        """Create a guest session (if enabled)"""
        if not self.config.get('enable_guest_mode', False):
            return {
                'success': False,
                'error': 'Guest mode is disabled'
            }
        
        # Create temporary guest user
        guest_id = f"guest_{int(time.time())}"
        session_id = self._generate_session_id()
        now = datetime.now()
        expires_at = now + timedelta(hours=2)  # Shorter timeout for guests
        
        session = Session(
            session_id=session_id,
            user_id=guest_id,
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            last_active=now.isoformat(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        sessions = self._load_sessions()
        sessions[session_id] = asdict(session)
        self._save_sessions(sessions)
        
        return {
            'success': True,
            'session_id': session_id,
            'user': {
                'user_id': guest_id,
                'email': 'guest@aipmtoolkit.local',
                'name': 'Guest User',
                'role': 'viewer',
                'preferences': {
                    'theme': 'light',
                    'default_experience': 'just_do_it'
                }
            },
            'expires_at': expires_at.isoformat(),
            'is_guest': True
        }

# Decorator for route protection
def require_auth(f):
    """Decorator to require authentication for routes"""
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify, g
        
        # Get session ID from header or cookie
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not session_id:
            session_id = request.cookies.get('aipm_session')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'login_required': True
            }), 401
        
        # Validate session
        auth_manager = AuthenticationManager()
        validation = auth_manager.validate_session(session_id)
        
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': validation['error'],
                'login_required': True
            }), 401
        
        # Add user info to request context
        g.current_user = validation['user']
        g.current_session = validation['session']
        
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            from flask import g, jsonify
            
            if not hasattr(g, 'current_user'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401
            
            user_role = g.current_user.get('role', 'viewer')
            
            # Role hierarchy: admin > pm > viewer
            role_hierarchy = {'viewer': 1, 'pm': 2, 'admin': 3}
            
            if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 999):
                return jsonify({
                    'success': False,
                    'error': f'Insufficient permissions. Required: {required_role}'
                }), 403
            
            return f(*args, **kwargs)
        
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator