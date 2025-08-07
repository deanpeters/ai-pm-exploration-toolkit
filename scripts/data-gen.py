#!/usr/bin/env python3
"""
AI PM Toolkit - Standalone Data Generation Script
Self-contained script for generating synthetic persona data

Usage:
    python data-gen.py                          # Interactive mode
    python data-gen.py --count=25 --type=b2b_saas --output=personas.json
    python data-gen.py --help                   # Show all options

This script can be copied to any project and used independently.
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

# Try to import faker, install if not available
try:
    from faker import Faker
except ImportError:
    print("📦 Installing Faker library for data generation...")
    os.system("pip install faker")
    from faker import Faker

# Self-contained persona generation (copied from shared module for independence)

@dataclass
class PersonaConfig:
    """Configuration for persona generation"""
    count: int = 10
    persona_type: str = "b2b_saas"
    include_demographics: bool = True
    include_psychographics: bool = True
    include_pain_points: bool = True
    include_goals: bool = True
    output_format: str = "json"

@dataclass
class Persona:
    """Individual persona data structure"""
    id: str
    name: str
    title: str
    company: str
    email: str
    demographics: Dict[str, Any]
    psychographics: Dict[str, Any]
    pain_points: List[str]
    goals: List[str]
    created_at: str

class StandaloneDataGenerator:
    """Self-contained data generation for maximum portability"""
    
    def __init__(self, working_dir: str = "."):
        self.fake = Faker()
        self.working_dir = Path(working_dir)
        
        # Persona templates - self-contained in this script
        self.persona_templates = {
            "b2b_saas": {
                "titles": [
                    "Product Manager", "VP of Product", "Director of Engineering", 
                    "Head of Growth", "CTO", "CEO", "Marketing Director",
                    "UX Research Lead", "Data Analyst", "Customer Success Manager"
                ],
                "pain_points": [
                    "Struggling with user adoption of new features",
                    "Difficulty measuring product-market fit",
                    "Engineering team is overloaded with feature requests",
                    "Limited budget for customer research",
                    "Competing priorities from different stakeholders",
                    "Lack of data-driven decision making processes",
                    "Integration challenges with third-party tools",
                    "Scaling customer support operations",
                    "Maintaining product quality while moving fast",
                    "Balancing technical debt with new features"
                ],
                "goals": [
                    "Increase user engagement by 25%",
                    "Reduce customer churn by 15%",
                    "Launch 3 new features this quarter",
                    "Improve customer satisfaction scores",
                    "Build data-driven product culture",
                    "Scale product team effectively",
                    "Implement automated testing pipeline",
                    "Expand into new market segments",
                    "Reduce time-to-market for features",
                    "Increase monthly recurring revenue"
                ]
            },
            "b2c_consumer": {
                "titles": [
                    "Marketing Manager", "Brand Manager", "Customer Experience Lead",
                    "Digital Marketing Specialist", "Content Creator", "Social Media Manager",
                    "E-commerce Manager", "Retail Operations", "Community Manager"
                ],
                "pain_points": [
                    "Hard to reach target demographic",
                    "Social media engagement declining",
                    "Customer acquisition costs increasing",
                    "Brand awareness low in key markets",
                    "Difficulty creating viral content",
                    "Seasonal sales fluctuations",
                    "Managing multiple marketing channels",
                    "Measuring ROI on marketing campaigns",
                    "Keeping up with platform algorithm changes",
                    "Competition from larger brands"
                ],
                "goals": [
                    "Increase brand awareness by 40%",
                    "Grow social media following by 50%",
                    "Launch successful influencer campaign",
                    "Improve customer lifetime value",
                    "Create compelling brand narrative",
                    "Expand to new market segments",
                    "Optimize conversion funnel",
                    "Build loyal customer community",
                    "Increase email subscriber base",
                    "Launch new product line successfully"
                ]
            }
        }
    
    def generate_persona(self, config: PersonaConfig) -> Persona:
        """Generate a single realistic persona"""
        template = self.persona_templates.get(config.persona_type, self.persona_templates["b2b_saas"])
        
        persona = Persona(
            id=f"persona_{self.fake.uuid4()[:8]}",
            name=self.fake.name(),
            title=random.choice(template["titles"]),
            company=self.fake.company(),
            email=self.fake.email(),
            demographics={},
            psychographics={},
            pain_points=[],
            goals=[],
            created_at=datetime.now().isoformat()
        )
        
        if config.include_demographics:
            persona.demographics = {
                "age": random.randint(25, 55),
                "location": f"{self.fake.city()}, {self.fake.state()}",
                "company_size": random.choice(["1-10", "11-50", "51-200", "201-1000", "1000+"]),
                "industry": random.choice([
                    "Technology", "Healthcare", "Finance", "Education", "Retail",
                    "Manufacturing", "Media", "Consulting", "Real Estate", "Non-profit"
                ]),
                "experience_years": random.randint(2, 20),
                "education": random.choice([
                    "Bachelor's Degree", "Master's Degree", "PhD", "Some College", "High School"
                ])
            }
        
        if config.include_psychographics:
            persona.psychographics = {
                "personality_type": random.choice(["Analytical", "Creative", "Pragmatic", "Visionary"]),
                "decision_style": random.choice(["Data-driven", "Intuitive", "Collaborative", "Independent"]),
                "tech_savviness": random.choice(["Low", "Medium", "High", "Expert"]),
                "risk_tolerance": random.choice(["Conservative", "Moderate", "Aggressive"]),
                "communication_preference": random.choice(["Email", "Slack", "Video calls", "In-person"]),
                "work_style": random.choice(["Remote", "Hybrid", "Office", "Flexible"]),
                "learning_preference": random.choice(["Visual", "Auditory", "Hands-on", "Reading"])
            }
        
        if config.include_pain_points:
            persona.pain_points = random.sample(
                template["pain_points"], 
                min(random.randint(2, 4), len(template["pain_points"]))
            )
        
        if config.include_goals:
            persona.goals = random.sample(
                template["goals"], 
                min(random.randint(2, 4), len(template["goals"]))
            )
        
        return persona
    
    def generate_personas(self, config: PersonaConfig) -> List[Persona]:
        """Generate multiple personas with variety"""
        personas = []
        for i in range(config.count):
            persona = self.generate_persona(config)
            personas.append(persona)
        return personas
    
    def save_personas(self, personas: List[Persona], filename: str, config: PersonaConfig) -> str:
        """Save personas to file in specified format"""
        output_path = self.working_dir / filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config.output_format == "json":
            data = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "generator": "AI PM Toolkit - Standalone Data Generator",
                    "version": "2.0.0",
                    "total_personas": len(personas)
                },
                "config": asdict(config),
                "personas": [asdict(p) for p in personas]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif config.output_format == "csv":
            import csv
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                header = [
                    'id', 'name', 'title', 'company', 'email', 'created_at',
                    'age', 'location', 'company_size', 'industry', 'experience_years', 'education',
                    'personality_type', 'decision_style', 'tech_savviness', 'risk_tolerance',
                    'communication_preference', 'work_style', 'learning_preference',
                    'pain_points', 'goals'
                ]
                writer.writerow(header)
                
                # Write data
                for p in personas:
                    row = [
                        p.id, p.name, p.title, p.company, p.email, p.created_at,
                        p.demographics.get('age', ''),
                        p.demographics.get('location', ''),
                        p.demographics.get('company_size', ''),
                        p.demographics.get('industry', ''),
                        p.demographics.get('experience_years', ''),
                        p.demographics.get('education', ''),
                        p.psychographics.get('personality_type', ''),
                        p.psychographics.get('decision_style', ''),
                        p.psychographics.get('tech_savviness', ''),
                        p.psychographics.get('risk_tolerance', ''),
                        p.psychographics.get('communication_preference', ''),
                        p.psychographics.get('work_style', ''),
                        p.psychographics.get('learning_preference', ''),
                        '; '.join(p.pain_points),
                        '; '.join(p.goals)
                    ]
                    writer.writerow(row)
        
        return str(output_path)
    
    def get_generation_stats(self, personas: List[Persona]) -> Dict[str, Any]:
        """Generate helpful statistics about the personas"""
        if not personas:
            return {}
        
        # Basic stats
        stats = {
            "total_personas": len(personas),
            "unique_companies": len(set(p.company for p in personas)),
            "generation_time": datetime.now().isoformat()
        }
        
        # Demographics analysis
        if personas[0].demographics:
            ages = [p.demographics.get('age', 0) for p in personas if p.demographics.get('age')]
            if ages:
                stats["age_range"] = {"min": min(ages), "max": max(ages), "avg": round(sum(ages) / len(ages), 1)}
            
            # Company size distribution
            company_sizes = [p.demographics.get('company_size') for p in personas if p.demographics.get('company_size')]
            stats["company_size_distribution"] = {size: company_sizes.count(size) for size in set(company_sizes)}
            
            # Industry distribution
            industries = [p.demographics.get('industry') for p in personas if p.demographics.get('industry')]
            stats["industry_distribution"] = {industry: industries.count(industry) for industry in set(industries)}
        
        # Title analysis
        titles = [p.title for p in personas]
        stats["title_distribution"] = {title: titles.count(title) for title in set(titles)}
        
        # Most common pain points and goals
        all_pain_points = []
        all_goals = []
        for p in personas:
            all_pain_points.extend(p.pain_points)
            all_goals.extend(p.goals)
        
        if all_pain_points:
            pain_counts = {pain: all_pain_points.count(pain) for pain in set(all_pain_points)}
            stats["top_pain_points"] = dict(sorted(pain_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        
        if all_goals:
            goal_counts = {goal: all_goals.count(goal) for goal in set(all_goals)}
            stats["top_goals"] = dict(sorted(goal_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        
        return stats

def interactive_mode():
    """Interactive mode for easy persona generation"""
    print("🎭 AI PM Toolkit - Interactive Data Generation")
    print("=" * 50)
    print()
    
    # Basic configuration
    print("Let's configure your persona generation:")
    print()
    
    # Count
    while True:
        try:
            count = int(input("How many personas? (default: 10): ") or "10")
            if count > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Type
    print("\nPersona types:")
    print("1. B2B SaaS (Product Managers, CTOs, Growth leads)")
    print("2. B2C Consumer (Marketing Managers, Brand leads)")
    
    while True:
        choice = input("Select type (1 or 2, default: 1): ") or "1"
        if choice in ["1", "2"]:
            persona_type = "b2b_saas" if choice == "1" else "b2c_consumer"
            break
        print("Please enter 1 or 2.")
    
    # Output format
    print("\nOutput formats:")
    print("1. JSON (structured data, good for analysis)")
    print("2. CSV (spreadsheet-friendly)")
    
    while True:
        choice = input("Select format (1 or 2, default: 1): ") or "1"
        if choice in ["1", "2"]:
            output_format = "json" if choice == "1" else "csv"
            break
        print("Please enter 1 or 2.")
    
    # Output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"personas_{persona_type}_{timestamp}.{output_format}"
    filename = input(f"Output filename (default: {default_name}): ") or default_name
    
    return {
        "count": count,
        "persona_type": persona_type,
        "output_format": output_format,
        "filename": filename
    }

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate synthetic persona data for product validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python data-gen.py                                    # Interactive mode
  python data-gen.py --count=25 --type=b2b_saas       # Quick generation
  python data-gen.py --count=50 --type=b2c_consumer --format=csv --output=marketing_personas.csv
  
This script generates realistic synthetic personas with:
  • Demographics (age, location, company info)
  • Psychographics (personality, work style)
  • Pain points and challenges
  • Goals and objectives

Perfect for:
  • Product validation without real user data
  • Testing UI/UX designs
  • Market research simulation
  • A/B testing scenarios
        """
    )
    
    # Optional arguments
    parser.add_argument("--count", type=int, default=None, 
                       help="Number of personas to generate")
    parser.add_argument("--type", choices=["b2b_saas", "b2c_consumer"], default=None,
                       help="Type of personas to generate")
    parser.add_argument("--format", choices=["json", "csv"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("--output", default=None,
                       help="Output filename")
    parser.add_argument("--dir", default=".", 
                       help="Output directory (default: current directory)")
    parser.add_argument("--interactive", action="store_true",
                       help="Force interactive mode")
    parser.add_argument("--quick", action="store_true",
                       help="Quick generation with defaults")
    
    args = parser.parse_args()
    
    # Determine mode
    if args.interactive or (not args.count and not args.quick):
        # Interactive mode
        config_dict = interactive_mode()
        config = PersonaConfig(
            count=config_dict["count"],
            persona_type=config_dict["persona_type"],
            output_format=config_dict["output_format"]
        )
        filename = config_dict["filename"]
    else:
        # Command line mode
        config = PersonaConfig(
            count=args.count or 10,
            persona_type=args.type or "b2b_saas",
            output_format=args.format
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = args.output or f"personas_{config.persona_type}_{timestamp}.{config.output_format}"
    
    try:
        # Generate personas
        print(f"\n🎭 Generating {config.count} {config.persona_type} personas...")
        
        generator = StandaloneDataGenerator(args.dir)
        personas = generator.generate_personas(config)
        
        # Save to file
        output_path = generator.save_personas(personas, filename, config)
        
        # Generate and show stats
        stats = generator.get_generation_stats(personas)
        
        print(f"✅ Generated {len(personas)} personas successfully!")
        print(f"📁 Saved to: {output_path}")
        print(f"📊 File size: {Path(output_path).stat().st_size:,} bytes")
        
        if stats:
            print(f"📈 Unique companies: {stats['unique_companies']}")
            if "age_range" in stats:
                age_range = stats["age_range"]
                print(f"👥 Age range: {age_range['min']}-{age_range['max']} (avg: {age_range['avg']})")
            
            if "top_pain_points" in stats:
                print(f"🔍 Top pain point: {list(stats['top_pain_points'].keys())[0]}")
        
        print(f"\n💡 Next steps:")
        print(f"   • Open {output_path} to explore your personas")
        print(f"   • Use this data for product validation and user research")
        print(f"   • Generate more data with different parameters as needed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()