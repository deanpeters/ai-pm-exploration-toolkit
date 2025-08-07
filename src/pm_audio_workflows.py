#!/usr/bin/env python3
"""
AI PM Toolkit - PM Audio Workflows
Phase 7.1: Pre-configured audio processing workflows for common PM scenarios
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from audio_transcription import AudioTranscriptionEngine, start_audio_transcription

@dataclass
class PMWorkflowTemplate:
    """Template for PM audio processing workflows"""
    id: str
    name: str
    description: str
    use_case: str
    recommended_model: str
    processing_steps: List[str]
    output_format: str
    typical_duration: str
    pm_insights_focus: List[str]

class PMAudioWorkflowEngine:
    """Engine for executing PM-specific audio workflows"""
    
    def __init__(self, working_dir: str = "."):
        self.working_dir = Path(working_dir)
        self.transcription_engine = AudioTranscriptionEngine(working_dir)
        
        # Define PM workflow templates
        self.workflow_templates = {
            "user_interview_analysis": PMWorkflowTemplate(
                id="user_interview_analysis",
                name="User Interview Deep Analysis",
                description="Comprehensive analysis of user interviews with pain point extraction and feature request identification",
                use_case="user_interviews",
                recommended_model="small",
                processing_steps=[
                    "Transcribe audio with high accuracy",
                    "Extract user pain points and frustrations",
                    "Identify feature requests and wishes", 
                    "Analyze user goals and objectives",
                    "Detect usability issues mentioned",
                    "Generate actionable PM insights summary"
                ],
                output_format="structured_insights",
                typical_duration="30-90 minutes",
                pm_insights_focus=["pain_points", "feature_requests", "user_goals", "usability_issues"]
            ),
            
            "stakeholder_meeting_summary": PMWorkflowTemplate(
                id="stakeholder_meeting_summary",
                name="Stakeholder Meeting Executive Summary",
                description="Generate executive summaries with decisions, action items, and next steps from stakeholder meetings",
                use_case="stakeholder_meetings", 
                recommended_model="medium",
                processing_steps=[
                    "Transcribe meeting with high accuracy",
                    "Extract key decisions made",
                    "Identify action items and ownership",
                    "Capture concerns and risks raised",
                    "Outline next steps and timelines",
                    "Generate executive summary report"
                ],
                output_format="executive_summary",
                typical_duration="45-120 minutes",
                pm_insights_focus=["decisions_made", "action_items", "concerns_raised", "next_steps"]
            ),
            
            "demo_feedback_analysis": PMWorkflowTemplate(
                id="demo_feedback_analysis",
                name="Product Demo Feedback Analysis",
                description="Analyze user reactions, questions, and suggestions from product demos",
                use_case="demo_feedback",
                recommended_model="base",
                processing_steps=[
                    "Transcribe demo session audio",
                    "Capture audience reactions and emotions",
                    "Extract questions asked during demo",
                    "Identify suggested improvements",
                    "Highlight positive feedback points",
                    "Create demo improvement recommendations"
                ],
                output_format="feedback_analysis",
                typical_duration="20-60 minutes", 
                pm_insights_focus=["reactions", "questions_asked", "suggested_improvements", "positive_feedback"]
            ),
            
            "competitive_research_notes": PMWorkflowTemplate(
                id="competitive_research_notes",
                name="Competitive Research & Analysis",
                description="Process competitor calls, presentations, or interviews for strategic insights",
                use_case="competitive_research",
                recommended_model="medium",
                processing_steps=[
                    "Transcribe competitor content",
                    "Extract key product features mentioned",
                    "Identify pricing and positioning strategies",
                    "Capture market approach insights",
                    "Analyze competitive advantages/weaknesses", 
                    "Generate competitive intelligence report"
                ],
                output_format="competitive_intelligence",
                typical_duration="30-90 minutes",
                pm_insights_focus=["product_features", "pricing_strategy", "market_positioning", "competitive_advantages"]
            ),
            
            "voice_memo_processing": PMWorkflowTemplate(
                id="voice_memo_processing",
                name="PM Voice Memo Processing",
                description="Convert PM voice memos into structured notes and action items",
                use_case="voice_memos",
                recommended_model="turbo",
                processing_steps=[
                    "Fast transcription of voice memo",
                    "Extract key ideas and concepts",
                    "Identify potential action items",
                    "Structure thoughts into categories",
                    "Generate follow-up task list",
                    "Create searchable notes format"
                ],
                output_format="structured_notes",
                typical_duration="5-30 minutes",
                pm_insights_focus=["key_ideas", "action_items", "follow_ups", "task_categories"]
            ),
            
            "customer_support_analysis": PMWorkflowTemplate(
                id="customer_support_analysis", 
                name="Customer Support Call Analysis",
                description="Analyze customer support calls for product insights and improvement opportunities",
                use_case="user_interviews",  # Reuse user interview analysis
                recommended_model="small",
                processing_steps=[
                    "Transcribe support call audio",
                    "Extract customer pain points",
                    "Identify product issues mentioned",
                    "Capture feature requests from customers",
                    "Analyze customer sentiment patterns",
                    "Generate product improvement recommendations"
                ],
                output_format="support_insights",
                typical_duration="15-45 minutes",
                pm_insights_focus=["customer_issues", "product_problems", "feature_requests", "sentiment_analysis"]
            )
        }
    
    def get_available_workflows(self) -> List[Dict[str, Any]]:
        """Get list of available PM workflow templates"""
        workflows = []
        for template in self.workflow_templates.values():
            workflows.append({
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "typical_duration": template.typical_duration,
                "recommended_model": template.recommended_model,
                "focus_areas": template.pm_insights_focus
            })
        return workflows
    
    def execute_workflow(self, workflow_id: str, audio_file: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific PM workflow on an audio file"""
        
        if workflow_id not in self.workflow_templates:
            return {
                "success": False,
                "error": f"Unknown workflow: {workflow_id}",
                "available_workflows": list(self.workflow_templates.keys())
            }
        
        template = self.workflow_templates[workflow_id]
        
        print(f"🎯 Executing PM Workflow: {template.name}")
        print(f"📄 Description: {template.description}")
        print(f"⏱️ Expected Duration: {template.typical_duration}")
        print(f"🤖 Using Model: {template.recommended_model}")
        print()
        
        # Execute transcription with template settings
        result = start_audio_transcription(
            audio_file,
            model=template.recommended_model,
            pm_use_case=template.use_case,
            working_dir=str(self.working_dir)
        )
        
        if result["success"]:
            # Enhance result with workflow-specific analysis
            enhanced_result = self._enhance_with_workflow_analysis(result, template)
            
            # Generate workflow-specific output
            workflow_output = self._generate_workflow_output(enhanced_result, template)
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "workflow_name": template.name,
                "transcription": enhanced_result["transcription"],
                "workflow_output": workflow_output,
                "processing_time": enhanced_result["processing_time"],
                "file_path": enhanced_result["file_path"]
            }
        else:
            return result
    
    def _enhance_with_workflow_analysis(self, result: Dict[str, Any], template: PMWorkflowTemplate) -> Dict[str, Any]:
        """Add workflow-specific analysis to transcription result"""
        
        enhanced_result = result.copy()
        transcription = enhanced_result["transcription"]
        pm_insights = transcription.get("pm_insights", {})
        
        # Add workflow metadata
        pm_insights["workflow_executed"] = {
            "id": template.id,
            "name": template.name,
            "focus_areas": template.pm_insights_focus,
            "processing_steps": template.processing_steps,
            "executed_at": datetime.now().isoformat()
        }
        
        # Enhance with workflow-specific scoring
        if "pm_specific_analysis" in pm_insights:
            analysis = pm_insights["pm_specific_analysis"]
            
            # Score the analysis based on workflow focus
            focus_score = 0
            total_insights = 0
            
            for focus_area in template.pm_insights_focus:
                if focus_area in analysis and analysis[focus_area]:
                    focus_score += len(analysis[focus_area])
                    total_insights += len(analysis[focus_area])
            
            pm_insights["workflow_analysis"] = {
                "focus_score": focus_score,
                "total_insights": total_insights,
                "relevance_rating": "high" if focus_score > 5 else "medium" if focus_score > 2 else "low",
                "key_findings_count": len([v for v in analysis.values() if v])
            }
        
        return enhanced_result
    
    def _generate_workflow_output(self, result: Dict[str, Any], template: PMWorkflowTemplate) -> Dict[str, Any]:
        """Generate workflow-specific formatted output"""
        
        transcription = result["transcription"]
        pm_insights = transcription.get("pm_insights", {})
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        
        output = {
            "workflow_name": template.name,
            "executed_at": datetime.now().isoformat(),
            "audio_duration": transcription.get("duration", 0),
            "processing_model": transcription.get("model_used"),
            "language": transcription.get("language"),
            "summary": self._generate_workflow_summary(transcription, template),
            "key_insights": {},
            "recommendations": [],
            "formatted_output": ""
        }
        
        # Extract key insights based on workflow focus
        for focus_area in template.pm_insights_focus:
            if focus_area in pm_analysis and pm_analysis[focus_area]:
                output["key_insights"][focus_area] = pm_analysis[focus_area]
        
        # Generate workflow-specific recommendations
        output["recommendations"] = self._generate_workflow_recommendations(pm_analysis, template)
        
        # Create formatted output based on template type
        if template.output_format == "executive_summary":
            output["formatted_output"] = self._format_executive_summary(transcription, template)
        elif template.output_format == "structured_insights":
            output["formatted_output"] = self._format_structured_insights(transcription, template) 
        elif template.output_format == "feedback_analysis":
            output["formatted_output"] = self._format_feedback_analysis(transcription, template)
        elif template.output_format == "competitive_intelligence":
            output["formatted_output"] = self._format_competitive_intelligence(transcription, template)
        elif template.output_format == "structured_notes":
            output["formatted_output"] = self._format_structured_notes(transcription, template)
        else:
            output["formatted_output"] = self._format_default_output(transcription, template)
        
        return output
    
    def _generate_workflow_summary(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Generate a workflow-specific summary"""
        
        pm_insights = transcription.get("pm_insights", {})
        duration_minutes = transcription.get("duration", 0) / 60
        word_count = pm_insights.get("word_count", 0)
        
        summary = f"""
{template.name} completed successfully.

Audio processed: {duration_minutes:.1f} minutes ({word_count} words)
Language: {transcription.get('language', 'Unknown')}
Model used: {transcription.get('model_used', 'Unknown')}

Focus areas analyzed: {', '.join(template.pm_insights_focus)}
Processing steps completed: {len(template.processing_steps)}
"""
        
        # Add workflow-specific summary details
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        if pm_analysis:
            summary += f"\nKey findings: {len([v for v in pm_analysis.values() if v])} categories with insights"
        
        return summary.strip()
    
    def _generate_workflow_recommendations(self, pm_analysis: Dict[str, Any], template: PMWorkflowTemplate) -> List[str]:
        """Generate workflow-specific recommendations"""
        
        recommendations = []
        
        if template.id == "user_interview_analysis":
            if pm_analysis.get("pain_points"):
                recommendations.append(f"Address {len(pm_analysis['pain_points'])} identified pain points in product roadmap")
            if pm_analysis.get("feature_requests"):
                recommendations.append(f"Evaluate {len(pm_analysis['feature_requests'])} feature requests for backlog prioritization")
        
        elif template.id == "stakeholder_meeting_summary":
            if pm_analysis.get("action_items"):
                recommendations.append(f"Track completion of {len(pm_analysis['action_items'])} identified action items")
            if pm_analysis.get("concerns_raised"):
                recommendations.append(f"Develop mitigation plans for {len(pm_analysis['concerns_raised'])} stakeholder concerns")
        
        elif template.id == "demo_feedback_analysis":
            if pm_analysis.get("suggested_improvements"):
                recommendations.append(f"Consider implementing {len(pm_analysis['suggested_improvements'])} suggested improvements")
            if pm_analysis.get("questions_asked"):
                recommendations.append(f"Prepare responses for {len(pm_analysis['questions_asked'])} common questions")
        
        # Add default recommendations if none generated
        if not recommendations:
            recommendations = [
                "Review transcription for additional insights",
                "Share findings with relevant team members",
                "Follow up on key points identified in the analysis"
            ]
        
        return recommendations
    
    def _format_executive_summary(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Format output as executive summary"""
        
        pm_insights = transcription.get("pm_insights", {})
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        
        summary = f"""# Executive Summary: {template.name}

**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Duration:** {transcription.get('duration', 0) / 60:.1f} minutes  
**Language:** {transcription.get('language', 'Unknown')}

## Key Decisions Made
"""
        
        if pm_analysis.get("decisions_made"):
            for decision in pm_analysis["decisions_made"][:5]:
                summary += f"- {decision}\n"
        else:
            summary += "- No specific decisions identified\n"
        
        summary += "\n## Action Items\n"
        
        if pm_analysis.get("action_items"):
            for action in pm_analysis["action_items"][:5]:
                summary += f"- {action}\n"
        else:
            summary += "- No specific action items identified\n"
        
        summary += "\n## Concerns & Risks\n"
        
        if pm_analysis.get("concerns_raised"):
            for concern in pm_analysis["concerns_raised"][:3]:
                summary += f"- {concern}\n"
        else:
            summary += "- No major concerns raised\n"
        
        summary += "\n## Next Steps\n"
        
        if pm_analysis.get("next_steps"):
            for step in pm_analysis["next_steps"][:3]:
                summary += f"- {step}\n"
        else:
            summary += "- Follow up meeting to be scheduled\n"
        
        return summary
    
    def _format_structured_insights(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Format output as structured user insights"""
        
        pm_insights = transcription.get("pm_insights", {})
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        
        insights = f"""# User Interview Insights: {template.name}

**Interview Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Duration:** {transcription.get('duration', 0) / 60:.1f} minutes  
**Word Count:** {pm_insights.get('word_count', 0)} words

## User Pain Points
"""
        
        if pm_analysis.get("pain_points"):
            for i, pain in enumerate(pm_analysis["pain_points"][:5], 1):
                insights += f"{i}. {pain}\n"
        else:
            insights += "- No specific pain points identified\n"
        
        insights += "\n## Feature Requests\n"
        
        if pm_analysis.get("feature_requests"):
            for i, request in enumerate(pm_analysis["feature_requests"][:5], 1):
                insights += f"{i}. {request}\n"
        else:
            insights += "- No feature requests identified\n"
        
        insights += "\n## User Goals\n"
        
        if pm_analysis.get("user_goals"):
            for i, goal in enumerate(pm_analysis["user_goals"][:3], 1):
                insights += f"{i}. {goal}\n"
        else:
            insights += "- User goals not clearly articulated\n"
        
        insights += "\n## Usability Issues\n"
        
        if pm_analysis.get("usability_issues"):
            for i, issue in enumerate(pm_analysis["usability_issues"][:3], 1):
                insights += f"{i}. {issue}\n"
        else:
            insights += "- No major usability issues mentioned\n"
        
        return insights
    
    def _format_feedback_analysis(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Format output as demo feedback analysis"""
        
        pm_insights = transcription.get("pm_insights", {})
        pm_analysis = pm_insights.get("pm_specific_analysis", {})
        
        feedback = f"""# Demo Feedback Analysis: {template.name}

**Demo Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Session Duration:** {transcription.get('duration', 0) / 60:.1f} minutes

## Audience Reactions
"""
        
        if pm_analysis.get("reactions"):
            for reaction in pm_analysis["reactions"][:5]:
                feedback += f"- {reaction}\n"
        else:
            feedback += "- No specific reactions captured\n"
        
        feedback += "\n## Questions Asked\n"
        
        if pm_analysis.get("questions_asked"):
            for question in pm_analysis["questions_asked"][:5]:
                feedback += f"- {question}\n"
        else:
            feedback += "- No questions were asked\n"
        
        feedback += "\n## Suggested Improvements\n"
        
        if pm_analysis.get("suggested_improvements"):
            for improvement in pm_analysis["suggested_improvements"][:5]:
                feedback += f"- {improvement}\n"
        else:
            feedback += "- No improvements suggested\n"
        
        feedback += "\n## Positive Feedback\n"
        
        if pm_analysis.get("positive_feedback"):
            for positive in pm_analysis["positive_feedback"][:3]:
                feedback += f"- {positive}\n"
        else:
            feedback += "- Limited positive feedback captured\n"
        
        return feedback
    
    def _format_competitive_intelligence(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Format output as competitive intelligence report"""
        
        text = transcription.get("text", "")
        
        intel = f"""# Competitive Intelligence Report: {template.name}

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Content Duration:** {transcription.get('duration', 0) / 60:.1f} minutes  
**Language:** {transcription.get('language', 'Unknown')}

## Key Competitive Insights

*Note: This is a basic analysis. For detailed competitive intelligence, consider using specialized tools.*

### Content Overview
{text[:500]}{'...' if len(text) > 500 else ''}

### Recommended Next Steps
- Conduct deeper analysis of competitive features mentioned
- Compare pricing and positioning strategies  
- Assess competitive threats and opportunities
- Update competitive landscape documentation

"""
        return intel
    
    def _format_structured_notes(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Format output as structured PM notes"""
        
        text = transcription.get("text", "")
        pm_insights = transcription.get("pm_insights", {})
        
        notes = f"""# PM Voice Memo Notes: {template.name}

**Recorded:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Duration:** {transcription.get('duration', 0) / 60:.1f} minutes  
**Words:** {pm_insights.get('word_count', 0)}

## Key Ideas Captured

{text}

## Potential Action Items

- Review and expand on ideas captured
- Prioritize follow-up actions
- Share relevant insights with team
- Schedule follow-up discussions if needed

## Tags
#pm-notes #voice-memo #product-ideas

"""
        return notes
    
    def _format_default_output(self, transcription: Dict[str, Any], template: PMWorkflowTemplate) -> str:
        """Default formatting for workflow output"""
        
        return f"""# {template.name} - Analysis Complete

**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Duration:** {transcription.get('duration', 0) / 60:.1f} minutes

## Transcription

{transcription.get('text', 'No transcription available')}

## Analysis Summary

The audio has been processed using the {template.name} workflow.
Check the PM insights section for specific findings related to: {', '.join(template.pm_insights_focus)}

"""

# Main function for CLI usage
def execute_pm_workflow(workflow_id: str, audio_file: str, working_dir: str = ".") -> Dict[str, Any]:
    """Execute a PM workflow - main entry point"""
    
    workflow_engine = PMAudioWorkflowEngine(working_dir)
    return workflow_engine.execute_workflow(workflow_id, audio_file)

# CLI entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI PM Toolkit - PM Audio Workflows")
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument("--workflow", help="Workflow ID to execute")
    parser.add_argument("--audio", help="Audio file to process")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    workflow_engine = PMAudioWorkflowEngine(".")
    
    if args.list:
        print("🎯 Available PM Audio Workflows")
        print("=" * 50)
        
        workflows = workflow_engine.get_available_workflows()
        for workflow in workflows:
            print(f"📋 {workflow['name']} (ID: {workflow['id']})")
            print(f"   {workflow['description']}")
            print(f"   Duration: {workflow['typical_duration']}")
            print(f"   Model: {workflow['recommended_model']}")
            print(f"   Focus: {', '.join(workflow['focus_areas'])}")
            print()
    
    elif args.workflow and args.audio:
        print(f"🎯 Executing PM Workflow: {args.workflow}")
        print(f"📁 Processing Audio: {args.audio}")
        
        if not os.path.exists(args.audio):
            print(f"❌ Error: Audio file not found: {args.audio}")
            exit(1)
        
        result = workflow_engine.execute_workflow(args.workflow, args.audio)
        
        if result["success"]:
            print("✅ Workflow completed successfully!")
            print(f"⏱️ Processing Time: {result['processing_time']:.1f}s")
            
            # Save output if specified
            if args.output:
                output_data = {
                    "workflow_result": result,
                    "generated_at": datetime.now().isoformat()
                }
                
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Results saved to: {args.output}")
            
            # Display key insights
            workflow_output = result["workflow_output"]
            print(f"\n📊 Key Insights: {len(workflow_output['key_insights'])} categories")
            print(f"💡 Recommendations: {len(workflow_output['recommendations'])}")
            
            print("\n📋 Formatted Output Preview:")
            print("-" * 50)
            print(workflow_output["formatted_output"][:500] + "...")
            
        else:
            print(f"❌ Workflow failed: {result['error']}")
    
    else:
        print("Usage: python3 pm_audio_workflows.py --list")
        print("       python3 pm_audio_workflows.py --workflow WORKFLOW_ID --audio AUDIO_FILE [--output OUTPUT_FILE]")
        print()
        print("Examples:")
        print("  python3 pm_audio_workflows.py --list")  
        print("  python3 pm_audio_workflows.py --workflow user_interview_analysis --audio interview.mp3")
        print("  python3 pm_audio_workflows.py --workflow stakeholder_meeting_summary --audio meeting.wav --output summary.json")