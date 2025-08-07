#!/usr/bin/env python3
"""
AI PM Toolkit - Shared AI Chat Engine
Local LLM integration for product manager assistance and brainstorming
"""

import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class ChatConfig:
    """Configuration for AI chat session"""
    model: str = "local"  # local, ollama, openai
    system_prompt: str = "You are a helpful AI assistant for product managers."
    max_tokens: int = 500
    temperature: float = 0.7
    chat_mode: str = "pm_assistant"  # pm_assistant, brainstorm, analysis
    save_conversation: bool = True
    working_dir: str = "."

@dataclass
class ChatMessage:
    """Individual chat message"""
    role: str  # user, assistant, system
    content: str
    timestamp: str
    tokens: Optional[int] = None

class AIChat:
    """Core AI chat engine for PM assistance"""
    
    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.conversation_history: List[ChatMessage] = []
        self.available_models = self._detect_available_models()
        
        # PM-specific system prompts
        self.system_prompts = {
            "pm_assistant": """You are an experienced product manager AI assistant. Help with:
- Product strategy and roadmap planning
- User research insights and persona development
- Feature prioritization and requirements gathering
- Market analysis and competitive intelligence
- Metrics definition and goal setting
- Stakeholder communication and alignment

Provide practical, actionable advice based on modern product management best practices.""",

            "brainstorm": """You are a creative brainstorming partner for product managers. Help generate:
- Innovative product ideas and features
- Creative solutions to user problems
- Alternative approaches to product challenges
- Market opportunity exploration
- User experience improvements

Be creative, ask follow-up questions, and build on ideas collaboratively.""",

            "analysis": """You are an analytical AI assistant for product managers. Help with:
- Data interpretation and insights
- Market research analysis
- Competitive landscape assessment
- User feedback synthesis
- Performance metrics evaluation
- Strategic decision support

Provide structured, data-driven analysis with clear recommendations."""
        }
    
    def _detect_available_models(self) -> Dict[str, bool]:
        """Detect which AI models/services are available"""
        models = {
            "ollama": False,
            "local_llm": False,
            "mock": True,  # Always available fallback
            "deepseek-r1": False,
            "llama3.2": False,
            "llama3.2-3b": False,
            "qwen2.5": False,  # Tool-calling model for Goose integration
            "gpt-oss-20b": False,  # OpenAI's latest reasoning model (when available)
            "gpt-oss-120b": False  # OpenAI's larger reasoning model (when available)
        }
        
        # Check for Ollama and available models
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models["ollama"] = True
                ollama_models = response.json().get("models", [])
                
                # Check for specific models we want to use
                for model_info in ollama_models:
                    model_name = model_info.get("name", "").lower()
                    if "deepseek-r1" in model_name:
                        models["deepseek-r1"] = True
                    elif "llama3.2" in model_name:
                        if "3b" in model_name:
                            models["llama3.2-3b"] = True
                        else:
                            models["llama3.2"] = True
                    elif "qwen2.5" in model_name:
                        models["qwen2.5"] = True
                    elif "gpt-oss-20b" in model_name:
                        models["gpt-oss-20b"] = True
                    elif "gpt-oss-120b" in model_name:
                        models["gpt-oss-120b"] = True
                            
        except Exception as e:
            print(f"Ollama detection error: {e}")
        
        return models
    
    def start_chat_session(self, config: ChatConfig) -> Dict[str, Any]:
        """Start a new chat session"""
        # Clear conversation history for new session
        self.conversation_history = []
        
        # Set system prompt based on chat mode
        system_prompt = self.system_prompts.get(config.chat_mode, config.system_prompt)
        
        # Add system message
        system_message = ChatMessage(
            role="system",
            content=system_prompt,
            timestamp=datetime.now().isoformat()
        )
        self.conversation_history.append(system_message)
        
        return {
            "session_id": f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "model": config.model,
            "chat_mode": config.chat_mode,
            "available_models": self.available_models,
            "system_prompt": system_prompt,
            "started_at": datetime.now().isoformat()
        }
    
    def send_message(self, message: str, config: ChatConfig) -> Dict[str, Any]:
        """Send a message and get AI response"""
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=message,
            timestamp=datetime.now().isoformat()
        )
        self.conversation_history.append(user_message)
        
        # Generate AI response - choose best available model
        if self.available_models.get("ollama"):
            response = self._chat_with_ollama(message, config)
        else:
            # Fallback to mock responses when Ollama not available
            response = self._generate_mock_response(message, config)
        
        # Add assistant response to history
        assistant_message = ChatMessage(
            role="assistant",
            content=response["content"],
            timestamp=datetime.now().isoformat(),
            tokens=response.get("tokens")
        )
        self.conversation_history.append(assistant_message)
        
        return {
            "response": response["content"],
            "tokens_used": response.get("tokens", 0),
            "model": config.model,
            "timestamp": assistant_message.timestamp,
            "conversation_length": len(self.conversation_history)
        }
    
    def _chat_with_ollama(self, message: str, config: ChatConfig) -> Dict[str, Any]:
        """Chat with Ollama local LLM using intelligent model selection"""
        try:
            # Select best available model based on requirements
            selected_model = self._select_best_model(config)
            
            # Prepare conversation context for Ollama
            messages = []
            for msg in self.conversation_history:
                if msg.role in ["user", "assistant", "system"]:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Configure model parameters based on chat mode
            model_options = {
                "temperature": config.temperature,
                "num_predict": config.max_tokens,
                "top_p": 0.9,
                "top_k": 40
            }
            
            # Adjust parameters for different chat modes
            if config.chat_mode == "analysis":
                model_options["temperature"] = min(0.3, config.temperature)  # More focused for analysis
            elif config.chat_mode == "brainstorm":
                model_options["temperature"] = max(0.8, config.temperature)  # More creative for brainstorming
            
            # Call Ollama API
            payload = {
                "model": selected_model,
                "messages": messages,
                "stream": False,
                "options": model_options
            }
            
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=payload,
                timeout=60  # Increased timeout for larger models
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result["message"]["content"],
                    "tokens": result.get("eval_count", 0),
                    "model": selected_model,
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                    "eval_duration": result.get("eval_duration", 0)
                }
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return self._generate_mock_response(message, config)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._generate_mock_response(message, config)
    
    def _select_best_model(self, config: ChatConfig) -> str:
        """Select the best available model based on chat requirements"""
        
        # For complex analysis and strategic thinking, prefer advanced reasoning models
        if config.chat_mode == "analysis":
            if self.available_models.get("gpt-oss-20b"):
                return "gpt-oss-20b"  # Best reasoning for analysis
            elif self.available_models.get("deepseek-r1"):
                return "deepseek-r1:7b"  # Fallback reasoning model
            elif self.available_models.get("qwen2.5"):
                return "qwen2.5"  # Tool-calling support for analysis
        
        # For PM assistant tasks, prefer advanced models with good reasoning
        if config.chat_mode == "pm_assistant":
            if self.available_models.get("gpt-oss-20b"):
                return "gpt-oss-20b"  # Advanced reasoning for PM tasks
            elif self.available_models.get("qwen2.5"):
                return "qwen2.5"  # Good for PM tasks with tool-calling
            elif self.available_models.get("llama3.2-3b"):
                return "llama3.2:3b"  # Fast responses
        
        # For creative brainstorming, prefer larger models
        if config.chat_mode == "brainstorm":
            if self.available_models.get("gpt-oss-20b"):
                return "gpt-oss-20b"  # Creative reasoning
            elif self.available_models.get("qwen2.5"):
                return "qwen2.5"  # Creative with tool-calling
            elif self.available_models.get("llama3.2"):
                return "llama3.2:latest"
            elif self.available_models.get("llama3.2-3b"):
                return "llama3.2:3b"
        
        # Fallback priority: gpt-oss-20b > qwen2.5 > DeepSeek R1 > Llama 3.2 > Llama 3.2 3B
        if self.available_models.get("gpt-oss-20b"):
            return "gpt-oss-20b"
        elif self.available_models.get("qwen2.5"):
            return "qwen2.5"
        elif self.available_models.get("deepseek-r1"):
            return "deepseek-r1:7b"
        elif self.available_models.get("llama3.2"):
            return "llama3.2:latest"
        elif self.available_models.get("llama3.2-3b"):
            return "llama3.2:3b"
        
        # Ultimate fallback
        return "llama3.2:3b"
    
    def _generate_mock_response(self, message: str, config: ChatConfig) -> Dict[str, Any]:
        """Generate mock AI responses for demonstration (Phase 3)"""
        
        # PM-specific response templates based on chat mode and message content
        message_lower = message.lower()
        
        if config.chat_mode == "pm_assistant":
            if any(word in message_lower for word in ["roadmap", "strategy", "plan"]):
                responses = [
                    "For effective roadmap planning, I recommend starting with your north star metrics and working backwards. What are the key outcomes you're trying to drive over the next 6-12 months?",
                    "A good product roadmap balances user value, business impact, and technical feasibility. Have you conducted user research to validate the problems you're solving?",
                    "Consider using the RICE framework (Reach, Impact, Confidence, Effort) to prioritize your roadmap items. What's your biggest constraint right now - resources, market timing, or technical complexity?"
                ]
            elif any(word in message_lower for word in ["user", "customer", "persona"]):
                responses = [
                    "Understanding your users is crucial for product success. I'd recommend conducting user interviews to gather qualitative insights. What user segments are you currently focusing on?",
                    "User personas should be based on real data, not assumptions. Have you analyzed your current user behavior and identified distinct usage patterns?",
                    "Consider mapping your user journey to identify pain points and opportunities. What's the most critical user workflow in your product?"
                ]
            elif any(word in message_lower for word in ["metrics", "kpi", "measure"]):
                responses = [
                    "Good product metrics should be actionable, accessible, and auditable. What business outcome are you trying to measure?",
                    "I recommend focusing on leading indicators rather than just lagging metrics. What user behaviors predict long-term success in your product?",
                    "Consider the HEART framework: Happiness, Engagement, Adoption, Retention, Task success. Which of these is most important for your current goals?"
                ]
            else:
                responses = [
                    "That's an interesting product challenge. Can you provide more context about your users and the specific problem you're trying to solve?",
                    "As a PM, it's important to validate assumptions with data. What evidence do you have to support this approach?",
                    "Let's think about this systematically. What are the key stakeholders involved and what are their needs?"
                ]
        
        elif config.chat_mode == "brainstorm":
            responses = [
                f"Building on your idea about '{message[:50]}...', what if we explored these angles: 1) How might we simplify this for new users? 2) What would the enterprise version look like? 3) How could we make this social or collaborative?",
                f"Interesting concept! Let's expand this thinking: What adjacent problems could we also solve? Who else might benefit from this solution? What would the minimal viable version look like?",
                f"Great starting point! Some creative directions to consider: Could we gamify this experience? What would the mobile-first approach be? How might AI enhance this workflow?"
            ]
        
        elif config.chat_mode == "analysis":
            responses = [
                "Based on typical product metrics, I'd recommend analyzing this through three lenses: user impact, business value, and technical feasibility. What data points are you working with?",
                "For thorough analysis, consider both quantitative metrics (usage, conversion, retention) and qualitative feedback (user interviews, support tickets). What trends are you seeing?",
                "Let's structure this analysis: 1) Current state assessment, 2) Root cause identification, 3) Impact evaluation, 4) Recommended actions. Where would you like to start?"
            ]
        
        else:
            responses = [
                "I'm here to help with your product management challenges. What specific area would you like to explore?",
                "As your AI product management assistant, I can help with strategy, user research, metrics, and more. What's on your mind?",
                "Let's dive into this topic. What's the context and what outcome are you hoping to achieve?"
            ]
        
        import random
        selected_response = random.choice(responses)
        
        return {
            "content": selected_response,
            "tokens": len(selected_response.split()) * 1.3,  # Approximate token count
            "model": "mock_pm_assistant"
        }
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        user_messages = [msg for msg in self.conversation_history if msg.role == "user"]
        assistant_messages = [msg for msg in self.conversation_history if msg.role == "assistant"]
        
        total_tokens = sum(msg.tokens or 0 for msg in self.conversation_history)
        
        return {
            "message_count": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_tokens": total_tokens,
            "conversation_start": self.conversation_history[0].timestamp if self.conversation_history else None,
            "last_message": self.conversation_history[-1].timestamp if self.conversation_history else None
        }
    
    def save_conversation(self, filename: str = None, session_id: str = None) -> str:
        """Save conversation to file with enhanced metadata"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_prefix = f"session_{session_id}_" if session_id else ""
            filename = f"ai_chat_{session_prefix}conversation_{timestamp}.json"
        
        # Create conversations directory
        conversations_dir = self.working_dir / "outputs" / "conversations"
        conversations_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = conversations_dir / filename
        
        # Enhanced conversation metadata
        conversation_data = {
            "metadata": {
                "session_id": session_id,
                "saved_at": datetime.now().isoformat(),
                "summary": self.get_conversation_summary(),
                "available_models": self.available_models,
                "conversation_topics": self._extract_conversation_topics(),
                "model_usage": self._get_model_usage_stats()
            },
            "messages": [asdict(msg) for msg in self.conversation_history]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def load_conversation(self, filename: str) -> bool:
        """Load conversation from file"""
        try:
            # Check if filename includes conversations directory
            if 'conversations/' in filename:
                file_path = self.working_dir / filename
            else:
                file_path = self.working_dir / "conversations" / filename
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.conversation_history = []
            for msg_data in data.get("messages", []):
                message = ChatMessage(**msg_data)
                self.conversation_history.append(message)
            
            return True
            
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False
    
    def _extract_conversation_topics(self) -> List[str]:
        """Extract key topics from conversation for search/categorization"""
        topics = []
        
        # Simple keyword extraction from user messages
        keywords = [
            "product management", "roadmap", "strategy", "metrics", "user research", 
            "prioritization", "stakeholders", "market", "competitive", "features",
            "requirements", "analytics", "customer", "business", "goals"
        ]
        
        conversation_text = " ".join([
            msg.content.lower() for msg in self.conversation_history 
            if msg.role == "user"
        ])
        
        for keyword in keywords:
            if keyword in conversation_text:
                topics.append(keyword)
        
        return topics[:5]  # Limit to top 5 topics
    
    def _get_model_usage_stats(self) -> Dict[str, int]:
        """Get statistics about model usage in this conversation"""
        model_counts = {}
        total_tokens = 0
        
        for msg in self.conversation_history:
            if msg.role == "assistant" and hasattr(msg, 'tokens') and msg.tokens:
                total_tokens += msg.tokens
        
        return {
            "total_tokens": total_tokens,
            "message_count": len(self.conversation_history),
            "assistant_messages": len([m for m in self.conversation_history if m.role == "assistant"])
        }
    
    def list_saved_conversations(self) -> List[Dict[str, Any]]:
        """List all saved conversations with metadata"""
        conversations_dir = self.working_dir / "conversations"
        if not conversations_dir.exists():
            return []
        
        conversations = []
        
        for file_path in conversations_dir.glob("ai_chat_*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                conversations.append({
                    "filename": file_path.name,
                    "saved_at": data["metadata"].get("saved_at"),
                    "message_count": data["metadata"]["summary"]["message_count"],
                    "topics": data["metadata"].get("conversation_topics", []),
                    "session_id": data["metadata"].get("session_id"),
                    "file_path": str(file_path)
                })
                
            except Exception as e:
                print(f"Error reading conversation file {file_path}: {e}")
                continue
        
        # Sort by save date, most recent first
        conversations.sort(key=lambda x: x["saved_at"] or "", reverse=True)
        return conversations
    
    def delete_conversation(self, filename: str) -> bool:
        """Delete a saved conversation"""
        try:
            conversations_dir = self.working_dir / "conversations"
            file_path = conversations_dir / filename
            
            if file_path.exists():
                file_path.unlink()
                return True
            
        except Exception as e:
            print(f"Error deleting conversation: {e}")
        
        return False

def start_ai_chat(chat_mode: str = "pm_assistant", model: str = "ollama", 
                 experience_type: str = "just_do_it", working_dir: str = ".") -> Dict[str, Any]:
    """Main entry point for AI chat - used by all interfaces"""
    
    chat_engine = AIChat(working_dir)
    
    # Configure based on experience type
    config = ChatConfig(
        model=model,
        chat_mode=chat_mode,
        temperature=0.7 if experience_type == "learn_and_do" else 0.5,
        max_tokens=300 if experience_type == "just_do_it" else 500,
        save_conversation=experience_type != "just_do_it",
        working_dir=working_dir
    )
    
    # Start session
    session_info = chat_engine.start_chat_session(config)
    
    return {
        "success": True,
        "session_info": session_info,
        "chat_engine": chat_engine,
        "config": asdict(config),
        "experience_type": experience_type
    }

# CLI entry point for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - AI Chat")
    parser.add_argument("--mode", choices=["pm_assistant", "brainstorm", "analysis"], 
                       default="pm_assistant", help="Chat mode")
    parser.add_argument("--model", choices=["local", "ollama"], default="local",
                       help="AI model to use")
    parser.add_argument("--interactive", action="store_true", help="Interactive chat mode")
    parser.add_argument("--dir", default=".", help="Working directory")
    
    args = parser.parse_args()
    
    try:
        # Start chat session
        result = start_ai_chat(
            chat_mode=args.mode,
            model=args.model,
            working_dir=args.dir
        )
        
        if result["success"]:
            chat_engine = result["chat_engine"]
            config = ChatConfig(**result["config"])
            
            print(f"🤖 AI PM Chat Started")
            print(f"Mode: {args.mode}")
            print(f"Model: {args.model}")
            print(f"Available models: {list(result['session_info']['available_models'].keys())}")
            print()
            
            if args.interactive:
                print("Type 'quit' to exit, 'save' to save conversation")
                print("=" * 50)
                
                while True:
                    try:
                        user_input = input("\nYou: ")
                        
                        if user_input.lower() in ['quit', 'exit']:
                            break
                        elif user_input.lower() == 'save':
                            filename = chat_engine.save_conversation()
                            print(f"💾 Conversation saved to: {filename}")
                            continue
                        
                        # Send message and get response
                        response = chat_engine.send_message(user_input, config)
                        print(f"\nAI: {response['response']}")
                        
                    except KeyboardInterrupt:
                        break
                
                # Save conversation on exit
                if config.save_conversation:
                    filename = chat_engine.save_conversation()
                    print(f"\n💾 Conversation saved to: {filename}")
            
            else:
                # Demo mode
                demo_messages = [
                    "How should I prioritize features for my product roadmap?",
                    "What metrics should I track for user engagement?",
                    "How do I validate this product idea with users?"
                ]
                
                for message in demo_messages:
                    print(f"\nDemo User: {message}")
                    response = chat_engine.send_message(message, config)
                    print(f"AI Assistant: {response['response']}")
                    print(f"[Tokens: {response['tokens_used']}]")
                
                if config.save_conversation:
                    filename = chat_engine.save_conversation()
                    print(f"\n💾 Demo conversation saved to: {filename}")
        
        else:
            print("❌ Chat session failed to start")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)