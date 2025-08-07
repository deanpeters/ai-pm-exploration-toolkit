#!/usr/bin/env python3
"""
AI PM Toolkit - Audio Transcription Engine
Phase 7.1: Audio Intelligence Integration for PM workflows
"""

import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import tempfile
import shutil

@dataclass
class TranscriptionResult:
    """Result of audio transcription"""
    text: str
    duration: float
    language: str
    segments: List[Dict[str, Any]]
    file_path: str
    model_used: str
    created_at: str
    processing_time: float
    pm_insights: Optional[Dict[str, Any]] = None

@dataclass
class AudioFile:
    """Audio file metadata"""
    path: str
    size: int
    duration: Optional[float]
    format: str
    created_at: str

class AudioTranscriptionEngine:
    """Core audio transcription engine for PM workflows"""
    
    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.transcripts_dir = self.working_dir / "outputs" / "transcripts"
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different PM use cases
        self.use_case_dirs = {
            "user_interviews": self.transcripts_dir / "user_interviews",
            "stakeholder_meetings": self.transcripts_dir / "stakeholder_meetings", 
            "demo_feedback": self.transcripts_dir / "demo_feedback",
            "competitive_research": self.transcripts_dir / "competitive_research",
            "voice_memos": self.transcripts_dir / "voice_memos",
            "general": self.transcripts_dir / "general"
        }
        
        for dir_path in self.use_case_dirs.values():
            dir_path.mkdir(exist_ok=True)
        
        # Available Whisper models (trade-off between speed and accuracy)
        self.available_models = {
            "turbo": {"size": "~80MB", "speed": "fastest", "accuracy": "good", "use_case": "quick voice memos"},
            "base": {"size": "~120MB", "speed": "fast", "accuracy": "better", "use_case": "general transcription"},
            "small": {"size": "~240MB", "speed": "medium", "accuracy": "good", "use_case": "user interviews"},
            "medium": {"size": "~770MB", "speed": "slow", "accuracy": "very good", "use_case": "stakeholder meetings"},
            "large": {"size": "~3GB", "speed": "slowest", "accuracy": "best", "use_case": "critical transcriptions"}
        }
    
    def check_whisper_availability(self) -> Dict[str, Any]:
        """Check if Whisper is available and working"""
        try:
            result = subprocess.run(
                ["whisper", "--help"], 
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "available": True,
                    "version": "latest",
                    "models": self.available_models,
                    "default_model": "turbo",
                    "output_formats": ["txt", "json", "vtt", "srt", "tsv"]
                }
            else:
                return {
                    "available": False,
                    "error": "Whisper command failed",
                    "install_command": "pip install openai-whisper"
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "install_command": "pip install openai-whisper"
            }
    
    def get_audio_info(self, audio_path: str) -> Optional[AudioFile]:
        """Get metadata about an audio file"""
        try:
            path_obj = Path(audio_path)
            if not path_obj.exists():
                return None
            
            return AudioFile(
                path=str(path_obj.absolute()),
                size=path_obj.stat().st_size,
                duration=None,  # Could use ffprobe to get duration
                format=path_obj.suffix.lower(),
                created_at=datetime.fromtimestamp(path_obj.stat().st_mtime).isoformat()
            )
            
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None
    
    def transcribe_audio(self, 
                        audio_path: str,
                        model: str = "turbo",
                        pm_use_case: str = "general",
                        language: Optional[str] = None,
                        output_format: str = "json") -> Optional[TranscriptionResult]:
        """Transcribe audio file with PM-specific optimizations"""
        
        start_time = time.time()
        
        try:
            # Validate inputs
            audio_file = self.get_audio_info(audio_path)
            if not audio_file:
                raise ValueError(f"Audio file not found: {audio_path}")
            
            if model not in self.available_models:
                model = "turbo"  # Fallback to fastest model
            
            # Create output directory for this use case
            output_dir = self.use_case_dirs.get(pm_use_case, self.use_case_dirs["general"])
            
            # Generate unique output filename
            audio_name = Path(audio_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{audio_name}_{timestamp}"
            
            # Build Whisper command with PM-optimized settings
            cmd = [
                "whisper",
                audio_path,
                "--model", model,
                "--output_dir", str(output_dir),
                "--output_format", output_format,
                "--verbose", "True"
            ]
            
            # Add language if specified
            if language:
                cmd.extend(["--language", language])
            
            # PM-specific optimizations
            if pm_use_case in ["user_interviews", "stakeholder_meetings"]:
                # Better accuracy for important meetings
                cmd.extend(["--temperature", "0"])
                cmd.extend(["--beam_size", "5"])
            elif pm_use_case == "voice_memos":
                # Faster processing for quick memos
                cmd.extend(["--temperature", "0.2"])
            
            # Execute Whisper transcription
            print(f"🎙️ Transcribing {Path(audio_path).name} using {model} model...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            processing_time = time.time() - start_time
            
            if result.returncode == 0:
                # Read the generated JSON file
                json_output_path = output_dir / f"{Path(audio_path).stem}.json"
                
                if json_output_path.exists():
                    with open(json_output_path, 'r', encoding='utf-8') as f:
                        whisper_result = json.load(f)
                    
                    # Create transcription result
                    transcription = TranscriptionResult(
                        text=whisper_result.get("text", ""),
                        duration=whisper_result.get("duration", 0.0),
                        language=whisper_result.get("language", "unknown"),
                        segments=whisper_result.get("segments", []),
                        file_path=str(json_output_path),
                        model_used=model,
                        created_at=datetime.now().isoformat(),
                        processing_time=processing_time,
                        pm_insights=self._extract_pm_insights(whisper_result, pm_use_case)
                    )
                    
                    # Save enhanced result with PM insights
                    enhanced_output_path = output_dir / f"{output_name}_enhanced.json"
                    with open(enhanced_output_path, 'w', encoding='utf-8') as f:
                        json.dump(asdict(transcription), f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Transcription completed in {processing_time:.1f}s")
                    print(f"📄 Result saved to: {enhanced_output_path}")
                    
                    return transcription
                else:
                    raise Exception("Whisper output file not found")
            else:
                raise Exception(f"Whisper failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def _extract_pm_insights(self, whisper_result: Dict[str, Any], pm_use_case: str) -> Dict[str, Any]:
        """Extract PM-specific insights from transcription"""
        
        text = whisper_result.get("text", "").lower()
        segments = whisper_result.get("segments", [])
        
        insights = {
            "use_case": pm_use_case,
            "word_count": len(whisper_result.get("text", "").split()),
            "speaking_rate": 0,  # words per minute
            "key_phrases": [],
            "potential_action_items": [],
            "sentiment_indicators": {},
            "pm_specific_analysis": {}
        }
        
        # Calculate speaking rate
        if whisper_result.get("duration", 0) > 0:
            insights["speaking_rate"] = round(insights["word_count"] / (whisper_result["duration"] / 60))
        
        # Extract PM-specific insights based on use case
        if pm_use_case == "user_interviews":
            insights["pm_specific_analysis"] = {
                "pain_points": self._find_pain_points(text),
                "feature_requests": self._find_feature_requests(text),
                "user_goals": self._find_user_goals(text),
                "usability_issues": self._find_usability_issues(text)
            }
        elif pm_use_case == "stakeholder_meetings":
            insights["pm_specific_analysis"] = {
                "decisions_made": self._find_decisions(text),
                "action_items": self._find_action_items(text),
                "concerns_raised": self._find_concerns(text),
                "next_steps": self._find_next_steps(text)
            }
        elif pm_use_case == "demo_feedback":
            insights["pm_specific_analysis"] = {
                "reactions": self._find_reactions(text),
                "questions_asked": self._find_questions(text),
                "suggested_improvements": self._find_improvements(text),
                "positive_feedback": self._find_positive_feedback(text)
            }
        
        return insights
    
    # PM-specific text analysis methods
    def _find_pain_points(self, text: str) -> List[str]:
        """Find potential pain points mentioned in user interviews"""
        pain_indicators = ["difficult", "hard", "frustrating", "annoying", "problem", "issue", "struggle", "confusing"]
        pain_points = []
        
        for indicator in pain_indicators:
            if indicator in text:
                # Find sentences containing pain indicators
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        pain_points.append(sentence.strip())
        
        return list(set(pain_points))[:5]  # Top 5 unique pain points
    
    def _find_feature_requests(self, text: str) -> List[str]:
        """Find feature requests in user interviews"""
        request_indicators = ["would like", "wish", "could you", "feature", "add", "include", "want"]
        requests = []
        
        for indicator in request_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        requests.append(sentence.strip())
        
        return list(set(requests))[:5]
    
    def _find_user_goals(self, text: str) -> List[str]:
        """Find user goals and objectives"""
        goal_indicators = ["trying to", "want to", "need to", "goal", "objective", "accomplish"]
        goals = []
        
        for indicator in goal_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        goals.append(sentence.strip())
        
        return list(set(goals))[:5]
    
    def _find_usability_issues(self, text: str) -> List[str]:
        """Find usability issues mentioned"""
        usability_indicators = ["can't find", "don't know how", "unclear", "confusing", "not obvious"]
        issues = []
        
        for indicator in usability_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        issues.append(sentence.strip())
        
        return list(set(issues))[:5]
    
    def _find_decisions(self, text: str) -> List[str]:
        """Find decisions made in meetings"""
        decision_indicators = ["decided", "agreed", "determined", "resolved", "settled"]
        decisions = []
        
        for indicator in decision_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        decisions.append(sentence.strip())
        
        return list(set(decisions))[:5]
    
    def _find_action_items(self, text: str) -> List[str]:
        """Find action items from meetings"""
        action_indicators = ["will do", "action item", "follow up", "next step", "assign", "responsible for"]
        actions = []
        
        for indicator in action_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        actions.append(sentence.strip())
        
        return list(set(actions))[:5]
    
    def _find_concerns(self, text: str) -> List[str]:
        """Find concerns raised in meetings"""
        concern_indicators = ["concerned", "worried", "risk", "issue", "problem", "challenge"]
        concerns = []
        
        for indicator in concern_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        concerns.append(sentence.strip())
        
        return list(set(concerns))[:5]
    
    def _find_next_steps(self, text: str) -> List[str]:
        """Find next steps from meetings"""
        next_step_indicators = ["next step", "next week", "follow up", "continue", "move forward"]
        steps = []
        
        for indicator in next_step_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        steps.append(sentence.strip())
        
        return list(set(steps))[:5]
    
    def _find_reactions(self, text: str) -> List[str]:
        """Find reactions to demos"""
        reaction_indicators = ["wow", "great", "interesting", "cool", "impressive", "concern", "question"]
        reactions = []
        
        for indicator in reaction_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        reactions.append(sentence.strip())
        
        return list(set(reactions))[:5]
    
    def _find_questions(self, text: str) -> List[str]:
        """Find questions asked during demos"""
        sentences = text.split('.')
        questions = []
        
        for sentence in sentences:
            if any(q in sentence for q in ["how", "what", "why", "when", "where", "can you"]):
                questions.append(sentence.strip())
        
        return list(set(questions))[:5]
    
    def _find_improvements(self, text: str) -> List[str]:
        """Find suggested improvements"""
        improvement_indicators = ["could improve", "better if", "suggest", "recommend", "enhance"]
        improvements = []
        
        for indicator in improvement_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        improvements.append(sentence.strip())
        
        return list(set(improvements))[:5]
    
    def _find_positive_feedback(self, text: str) -> List[str]:
        """Find positive feedback"""
        positive_indicators = ["like", "love", "great", "excellent", "good", "helpful", "useful"]
        feedback = []
        
        for indicator in positive_indicators:
            if indicator in text:
                sentences = text.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        feedback.append(sentence.strip())
        
        return list(set(feedback))[:5]
    
    def batch_transcribe(self, audio_directory: str, 
                        model: str = "turbo",
                        pm_use_case: str = "general") -> List[TranscriptionResult]:
        """Batch transcribe all audio files in a directory"""
        
        audio_dir = Path(audio_directory)
        if not audio_dir.exists():
            raise ValueError(f"Directory not found: {audio_directory}")
        
        # Supported audio formats
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}
        
        # Find all audio files
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(audio_dir.glob(f"*{ext}"))
            audio_files.extend(audio_dir.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            print(f"No audio files found in {audio_directory}")
            return []
        
        print(f"Found {len(audio_files)} audio files to transcribe...")
        
        results = []
        for i, audio_file in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {audio_file.name}")
            
            result = self.transcribe_audio(
                str(audio_file),
                model=model,
                pm_use_case=pm_use_case
            )
            
            if result:
                results.append(result)
            
            # Brief pause between files
            time.sleep(1)
        
        print(f"✅ Batch transcription completed: {len(results)}/{len(audio_files)} successful")
        return results
    
    def get_transcription_history(self, pm_use_case: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get history of transcriptions"""
        
        if pm_use_case:
            search_dirs = [self.use_case_dirs.get(pm_use_case, self.use_case_dirs["general"])]
        else:
            search_dirs = list(self.use_case_dirs.values())
        
        history = []
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for json_file in search_dir.glob("*_enhanced.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            history.append({
                                "file": json_file.name,
                                "created_at": data.get("created_at"),
                                "model_used": data.get("model_used"),
                                "duration": data.get("duration"),
                                "word_count": data.get("pm_insights", {}).get("word_count", 0),
                                "use_case": data.get("pm_insights", {}).get("use_case", "unknown"),
                                "path": str(json_file)
                            })
                    except Exception as e:
                        continue
        
        # Sort by creation time, most recent first
        history.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return history
    
    def generate_pm_summary(self, transcription: TranscriptionResult) -> str:
        """Generate a PM-focused summary of the transcription"""
        
        pm_insights = transcription.pm_insights or {}
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        
        summary = f"""
# Audio Transcription Summary

**File**: {Path(transcription.file_path).stem}
**Duration**: {transcription.duration:.1f} seconds ({transcription.duration/60:.1f} minutes)
**Model Used**: {transcription.model_used}
**Language**: {transcription.language}
**Word Count**: {pm_insights.get('word_count', 0)} words
**Speaking Rate**: {pm_insights.get('speaking_rate', 0)} words per minute

## Key Insights

"""
        
        if transcription.pm_insights:
            use_case = pm_insights.get('use_case', 'general')
            
            if use_case == "user_interviews":
                summary += "### User Interview Analysis\n\n"
                if pm_analysis.get('pain_points'):
                    summary += "**Pain Points Mentioned:**\n"
                    for pain in pm_analysis['pain_points']:
                        summary += f"- {pain}\n"
                    summary += "\n"
                
                if pm_analysis.get('feature_requests'):
                    summary += "**Feature Requests:**\n"
                    for request in pm_analysis['feature_requests']:
                        summary += f"- {request}\n"
                    summary += "\n"
            
            elif use_case == "stakeholder_meetings":
                summary += "### Meeting Analysis\n\n"
                if pm_analysis.get('decisions_made'):
                    summary += "**Decisions Made:**\n"
                    for decision in pm_analysis['decisions_made']:
                        summary += f"- {decision}\n"
                    summary += "\n"
                
                if pm_analysis.get('action_items'):
                    summary += "**Action Items:**\n"
                    for action in pm_analysis['action_items']:
                        summary += f"- {action}\n"
                    summary += "\n"
        
        summary += f"""
## Full Transcription

{transcription.text}

---
*Generated by AI PM Toolkit Audio Intelligence*
*Processed at: {transcription.created_at}*
"""
        
        return summary

def start_audio_transcription(audio_file: str, model: str = "turbo", 
                            pm_use_case: str = "general", 
                            working_dir: str = ".") -> Dict[str, Any]:
    """Main entry point for audio transcription - used by CLI and web interfaces"""
    
    engine = AudioTranscriptionEngine(working_dir)
    
    # Check Whisper availability
    availability = engine.check_whisper_availability()
    if not availability["available"]:
        return {
            "success": False,
            "error": availability["error"],
            "install_command": availability.get("install_command")
        }
    
    # Perform transcription
    result = engine.transcribe_audio(audio_file, model, pm_use_case)
    
    if result:
        # Generate PM summary
        summary = engine.generate_pm_summary(result)
        
        return {
            "success": True,
            "transcription": asdict(result),
            "summary": summary,
            "file_path": result.file_path,
            "processing_time": result.processing_time
        }
    else:
        return {
            "success": False,
            "error": "Transcription failed"
        }

# CLI entry point for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - Audio Transcription")
    parser.add_argument("audio_file", nargs="?", help="Path to audio file to transcribe")
    parser.add_argument("--model", choices=["turbo", "base", "small", "medium", "large"], 
                       default="turbo", help="Whisper model to use")
    parser.add_argument("--use-case", choices=["user_interviews", "stakeholder_meetings", 
                                             "demo_feedback", "competitive_research", 
                                             "voice_memos", "general"], 
                       default="general", help="PM use case for optimized analysis")
    parser.add_argument("--language", help="Language of the audio (auto-detect if not specified)")
    parser.add_argument("--batch", help="Transcribe all audio files in directory")
    parser.add_argument("--history", action="store_true", help="Show transcription history")
    parser.add_argument("--status", action="store_true", help="Check Whisper status")
    
    args = parser.parse_args()
    
    engine = AudioTranscriptionEngine(".")
    
    if args.status:
        status = engine.check_whisper_availability()
        print("🎙️ Audio Transcription Status")
        print("=" * 40)
        print(f"Whisper Available: {'✅' if status['available'] else '❌'}")
        if status["available"]:
            print(f"Default Model: {status['default_model']}")
            print("Available Models:")
            for model, info in status["models"].items():
                print(f"  • {model}: {info['size']} - {info['accuracy']} accuracy ({info['use_case']})")
        else:
            print(f"Error: {status['error']}")
            print(f"Install: {status.get('install_command', 'N/A')}")
    
    elif args.history:
        history = engine.get_transcription_history()
        print("📋 Transcription History")
        print("=" * 40)
        if history:
            for item in history[:10]:  # Show last 10
                print(f"📄 {item['file']}")
                print(f"   Use Case: {item['use_case']}")
                print(f"   Duration: {item['duration']:.1f}s, Words: {item['word_count']}")
                print(f"   Model: {item['model_used']}, Created: {item['created_at'][:10]}")
                print()
        else:
            print("No transcriptions found")
    
    elif args.batch:
        print(f"🎙️ Batch Transcribing: {args.batch}")
        results = engine.batch_transcribe(args.batch, args.model, args.use_case)
        print(f"✅ Completed: {len(results)} transcriptions")
    
    else:
        print(f"🎙️ Transcribing: {args.audio_file}")
        result = engine.transcribe_audio(
            args.audio_file, 
            model=args.model, 
            pm_use_case=args.use_case,
            language=args.language
        )
        
        if result:
            print("✅ Transcription completed!")
            print(f"📄 Text: {result.text[:200]}...")
            print(f"⏱️ Duration: {result.duration:.1f}s")
            print(f"📊 Processing Time: {result.processing_time:.1f}s")
            print(f"💬 Language: {result.language}")
            print(f"📝 Words: {result.pm_insights.get('word_count', 0)} words")
            
            # Show PM insights
            if result.pm_insights and result.pm_insights.get('pm_specific_analysis'):
                print("\n🔍 PM Insights:")
                analysis = result.pm_insights['pm_specific_analysis']
                for key, values in analysis.items():
                    if values:
                        print(f"  {key.replace('_', ' ').title()}: {len(values)} found")
        else:
            print("❌ Transcription failed")