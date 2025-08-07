#!/usr/bin/env python3
"""
AI PM Toolkit - Shared Data Generation Logic
Used by web, CLI, and standalone interfaces
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Try to import faker, install if not available
try:
    from faker import Faker
except ImportError:
    print("📦 Installing Faker library for data generation...")
    os.system("pip install faker")
    from faker import Faker

@dataclass
class PersonaConfig:
    """Configuration for persona generation"""
    count: int = 10
    persona_type: str = "b2b_saas"  # b2b_saas, b2c_consumer, startup, enterprise
    include_demographics: bool = True
    include_psychographics: bool = True
    include_pain_points: bool = True
    include_goals: bool = True
    output_format: str = "json"  # json, csv, yaml

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

class DataGenerator:
    """Core data generation engine"""
    
    def __init__(self, working_dir: str = "."):
        self.fake = Faker()
        self.working_dir = Path(working_dir)
        self.persona_templates = {
            "b2b_saas": {
                "titles": ["Product Manager", "VP of Product", "Director of Engineering", 
                          "Head of Growth", "CTO", "CEO", "Marketing Director"],
                "pain_points": [
                    "Struggling with user adoption of new features",
                    "Difficulty measuring product-market fit",
                    "Engineering team is overloaded with feature requests",
                    "Limited budget for customer research",
                    "Competing priorities from different stakeholders",
                    "Lack of data-driven decision making processes"
                ],
                "goals": [
                    "Increase user engagement by 25%",
                    "Reduce customer churn by 15%",
                    "Launch 3 new features this quarter",
                    "Improve customer satisfaction scores",
                    "Build data-driven product culture",
                    "Scale product team effectively"
                ]
            },
            "b2c_consumer": {
                "titles": ["Marketing Manager", "Brand Manager", "Customer Experience Lead",
                          "Digital Marketing Specialist", "Content Creator", "Social Media Manager"],
                "pain_points": [
                    "Hard to reach target demographic",
                    "Social media engagement declining",
                    "Customer acquisition costs increasing",
                    "Brand awareness low in key markets",
                    "Difficulty creating viral content",
                    "Seasonal sales fluctuations"
                ],
                "goals": [
                    "Increase brand awareness by 40%",
                    "Grow social media following by 50%",
                    "Launch successful influencer campaign",
                    "Improve customer lifetime value",
                    "Create compelling brand narrative",
                    "Expand to new market segments"
                ]
            }
        }

    def generate_persona(self, config: PersonaConfig) -> Persona:
        """Generate a single persona"""
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
                "industry": self.fake.bs().split()[0].capitalize(),
                "experience_years": random.randint(2, 20)
            }
        
        if config.include_psychographics:
            persona.psychographics = {
                "personality_type": random.choice(["Analytical", "Creative", "Pragmatic", "Visionary"]),
                "decision_style": random.choice(["Data-driven", "Intuitive", "Collaborative", "Independent"]),
                "tech_savviness": random.choice(["Low", "Medium", "High", "Expert"]),
                "risk_tolerance": random.choice(["Conservative", "Moderate", "Aggressive"]),
                "communication_preference": random.choice(["Email", "Slack", "Video calls", "In-person"])
            }
        
        if config.include_pain_points:
            persona.pain_points = random.sample(template["pain_points"], 
                                               min(3, len(template["pain_points"])))
        
        if config.include_goals:
            persona.goals = random.sample(template["goals"], 
                                        min(3, len(template["goals"])))
        
        return persona

    def generate_personas(self, config: PersonaConfig) -> List[Persona]:
        """Generate multiple personas"""
        return [self.generate_persona(config) for _ in range(config.count)]

    def save_personas(self, personas: List[Persona], filename: str, config: PersonaConfig) -> str:
        """Save personas to file in specified format"""
        output_path = self.working_dir / "outputs" / "personas" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config.output_format == "json":
            data = {
                "generated_at": datetime.now().isoformat(),
                "config": asdict(config),
                "personas": [asdict(p) for p in personas]
            }
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        elif config.output_format == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow([
                    'id', 'name', 'title', 'company', 'email', 'age', 'location',
                    'company_size', 'industry', 'personality_type', 'decision_style',
                    'pain_points', 'goals'
                ])
                # Write data
                for p in personas:
                    writer.writerow([
                        p.id, p.name, p.title, p.company, p.email,
                        p.demographics.get('age', ''), p.demographics.get('location', ''),
                        p.demographics.get('company_size', ''), p.demographics.get('industry', ''),
                        p.psychographics.get('personality_type', ''), p.psychographics.get('decision_style', ''),
                        '; '.join(p.pain_points), '; '.join(p.goals)
                    ])
        
        return str(output_path)

    def get_generation_stats(self, personas: List[Persona]) -> Dict[str, Any]:
        """Generate statistics about the created personas"""
        if not personas:
            return {}
        
        # Company size distribution
        company_sizes = [p.demographics.get('company_size', 'Unknown') for p in personas if p.demographics]
        company_size_dist = {size: company_sizes.count(size) for size in set(company_sizes)}
        
        # Title distribution
        titles = [p.title for p in personas]
        title_dist = {title: titles.count(title) for title in set(titles)}
        
        # Average age
        ages = [p.demographics.get('age', 0) for p in personas if p.demographics and p.demographics.get('age')]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        return {
            "total_personas": len(personas),
            "company_size_distribution": company_size_dist,
            "title_distribution": title_dist,
            "average_age": round(avg_age, 1) if avg_age else None,
            "unique_companies": len(set(p.company for p in personas)),
            "common_pain_points": self._get_common_items([p.pain_points for p in personas]),
            "common_goals": self._get_common_items([p.goals for p in personas])
        }
    
    def _get_common_items(self, item_lists: List[List[str]], top_n: int = 5) -> Dict[str, int]:
        """Get most common items across all lists"""
        all_items = []
        for item_list in item_lists:
            all_items.extend(item_list)
        
        item_counts = {item: all_items.count(item) for item in set(all_items)}
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_items[:top_n])

def generate_sample_data(experience_type: str = "just_do_it", working_dir: str = ".", 
                        count: int = 10, persona_type: str = "b2b_saas") -> Dict[str, Any]:
    """Main entry point for data generation - used by all interfaces"""
    
    generator = DataGenerator(working_dir)
    
    # Configure based on experience type
    if experience_type == "just_do_it":
        config = PersonaConfig(count=count, persona_type=persona_type)
        filename = f"personas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    elif experience_type == "learn_and_do":
        config = PersonaConfig(
            count=count, 
            persona_type=persona_type,
            include_demographics=True,
            include_psychographics=True,
            include_pain_points=True,
            include_goals=True
        )
        filename = f"personas_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    else:  # cli_deep_dive
        config = PersonaConfig(
            count=count,
            persona_type=persona_type,
            output_format="json"  # CLI will handle format choice
        )
        filename = f"personas_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Generate personas
    print(f"🎭 Generating {count} {persona_type} personas...")
    personas = generator.generate_personas(config)
    
    # Save to file
    output_path = generator.save_personas(personas, filename, config)
    
    # Generate stats
    stats = generator.get_generation_stats(personas)
    
    return {
        "success": True,
        "output_file": output_path,
        "config": asdict(config),
        "stats": stats,
        "sample_persona": asdict(personas[0]) if personas else None,
        "experience_type": experience_type
    }

# CLI entry point for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic persona data")
    parser.add_argument("--count", type=int, default=10, help="Number of personas to generate")
    parser.add_argument("--type", choices=["b2b_saas", "b2c_consumer"], default="b2b_saas", 
                       help="Type of personas to generate")
    parser.add_argument("--experience", choices=["just_do_it", "learn_and_do", "cli_deep_dive"], 
                       default="just_do_it", help="Experience type")
    parser.add_argument("--dir", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    result = generate_sample_data(
        experience_type=args.experience,
        working_dir=args.dir,
        count=args.count,
        persona_type=args.type
    )
    
    if result["success"]:
        print(f"✅ Generated {result['stats']['total_personas']} personas")
        print(f"📁 Saved to: {result['output_file']}")
        print(f"📊 Stats: {json.dumps(result['stats'], indent=2)}")
    else:
        print("❌ Generation failed")