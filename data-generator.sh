#!/bin/bash
# AI PM Toolkit - Data Generator Script
# Simple data generation for testing and validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 AI PM Toolkit - Data Generator${NC}"
echo "========================================"

# Check if we have any data generation tools available
echo -e "${YELLOW}🔍 Checking available data generation tools...${NC}"

AVAILABLE_TOOLS=()

# Check for Python and faker
if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import faker" 2>/dev/null; then
        AVAILABLE_TOOLS+=("faker")
        echo -e "${GREEN}✅ Python Faker - Available${NC}"
    else
        echo -e "${YELLOW}⚠️  Python Faker - Install with: pip3 install faker${NC}"
    fi
else
    echo -e "${RED}❌ Python3 - Not available${NC}"
fi

# Check for Jupyter
if command -v jupyter >/dev/null 2>&1; then
    AVAILABLE_TOOLS+=("jupyter")
    echo -e "${GREEN}✅ Jupyter Lab - Available${NC}"
else
    echo -e "${YELLOW}⚠️  Jupyter Lab - Install with: pip3 install jupyterlab${NC}"
fi

echo

if [ ${#AVAILABLE_TOOLS[@]} -eq 0 ]; then
    echo -e "${RED}❌ No data generation tools available${NC}"
    echo
    echo -e "${YELLOW}💡 Install data generation tools:${NC}"
    echo "  pip3 install faker mimesis jupyterlab pandas"
    echo
    echo -e "${YELLOW}💡 Alternative options:${NC}"
    echo "  • Launch Jupyter Lab: aipm_lab"
    echo "  • Use AI collaboration: aipm_brainstorm"
    exit 1
fi

echo -e "${BLUE}🎯 Available Data Generation Options:${NC}"
echo
echo "1. 👥 Generate User Personas (Faker)"
echo "2. 📧 Generate Sample Email Data"  
echo "3. 🏢 Generate Company Data"
echo "4. 💳 Generate Transaction Data"
echo "5. 📊 Launch Jupyter Lab for Custom Generation"
echo "6. 🤖 AI-Assisted Data Generation"
echo "7. Exit"
echo

read -p "Choose option (1-7): " choice

case $choice in
    1)
        echo -e "${YELLOW}👥 Generating User Personas...${NC}"
        python3 -c "
import faker
import json
from datetime import datetime

fake = faker.Faker()
personas = []

for i in range(10):
    persona = {
        'id': i + 1,
        'name': fake.name(),
        'email': fake.email(),
        'job_title': fake.job(),
        'company': fake.company(),
        'age': fake.random_int(25, 65),
        'location': f'{fake.city()}, {fake.state()}',
        'bio': fake.text(max_nb_chars=200),
        'pain_points': [fake.sentence() for _ in range(3)],
        'goals': [fake.sentence() for _ in range(2)]
    }
    personas.append(persona)

print('Generated 10 User Personas:')
print(json.dumps(personas, indent=2))

# Save to file
with open('user_personas.json', 'w') as f:
    json.dump(personas, f, indent=2)
print('\n✅ Saved to user_personas.json')
"
        ;;
    2)
        echo -e "${YELLOW}📧 Generating Email Data...${NC}"
        python3 -c "
import faker
import csv
from datetime import datetime, timedelta

fake = faker.Faker()

with open('sample_emails.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['sender', 'recipient', 'subject', 'timestamp', 'category'])
    
    categories = ['support', 'sales', 'newsletter', 'notification', 'personal']
    
    for i in range(100):
        writer.writerow([
            fake.email(),
            fake.email(),
            fake.sentence(nb_words=6),
            fake.date_time_between(start_date='-30d', end_date='now'),
            fake.random_element(categories)
        ])

print('✅ Generated 100 sample emails in sample_emails.csv')
"
        ;;
    3)
        echo -e "${YELLOW}🏢 Generating Company Data...${NC}"
        python3 -c "
import faker
import json

fake = faker.Faker()
companies = []

industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education']

for i in range(20):
    company = {
        'id': i + 1,
        'name': fake.company(),
        'industry': fake.random_element(industries),
        'employees': fake.random_int(10, 10000),
        'revenue': fake.random_int(100000, 100000000),
        'founded': fake.random_int(1990, 2020),
        'location': f'{fake.city()}, {fake.state()}',
        'website': fake.url(),
        'description': fake.text(max_nb_chars=300)
    }
    companies.append(company)

print('Generated 20 Companies:')
print(json.dumps(companies, indent=2))

with open('companies.json', 'w') as f:
    json.dump(companies, f, indent=2)
print('\n✅ Saved to companies.json')
"
        ;;
    4)
        echo -e "${YELLOW}💳 Generating Transaction Data...${NC}"
        python3 -c "
import faker
import csv
from datetime import datetime

fake = faker.Faker()

with open('transactions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['transaction_id', 'user_id', 'amount', 'currency', 'timestamp', 'category', 'status'])
    
    categories = ['subscription', 'one-time', 'upgrade', 'addon', 'refund']
    statuses = ['completed', 'pending', 'failed', 'cancelled']
    
    for i in range(500):
        writer.writerow([
            fake.uuid4(),
            fake.random_int(1, 1000),
            round(fake.random.uniform(5.99, 999.99), 2),
            'USD',
            fake.date_time_between(start_date='-90d', end_date='now'),
            fake.random_element(categories),
            fake.random_element(statuses)
        ])

print('✅ Generated 500 transactions in transactions.csv')
"
        ;;
    5)
        echo -e "${YELLOW}📊 Launching Jupyter Lab...${NC}"
        echo "Create custom data generation in Jupyter Lab"
        aipm_lab
        ;;
    6)
        echo -e "${YELLOW}🤖 Starting AI-Assisted Data Generation...${NC}"
        echo "Use AI to help create custom datasets"
        aipm_brainstorm
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option"
        ;;
esac

echo
echo -e "${GREEN}✅ Data generation complete!${NC}"
echo
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "  • Analyze data: aipm_lab"
echo "  • Visualize results: aipm_design"
echo "  • Document findings: aipm_knowledge"