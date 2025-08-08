# HOW2TEST_EVERYTHING_MANUALLY.md

# CLEANUP & SETUP
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh stop
docker system prune -f
rm -f /Users/deanpeters/ai-pm-toolkit/aipm-env.sh
cd /Users/deanpeters/ai-pm-exploration-toolkit
python3 core/installer.py --status
source ~/.bashrc && source ~/.zshrc

# CORE CLI TESTS (from ~/temp)
mkdir -p ~/temp && cd ~/temp

# Test 1: Data Generation Commands
aipm data-gen --count=5 --type=b2b_saas
aipm data-gen --count=3 --type=b2c_consumer
python3 /Users/deanpeters/ai-pm-exploration-toolkit/src/data_generator.py --count=2 --type=b2b_saas

# Test 2: Market Research Commands
aipm research --type=company --company="MSFT"
aipm research --type=company --ticker="AAPL"
python3 /Users/deanpeters/ai-pm-exploration-toolkit/src/market_research.py --type=company --company="Tesla"

# Test 3: Audio Intelligence (Status Check)
python3 /Users/deanpeters/ai-pm-exploration-toolkit/src/audio_transcription.py --status
python3 /Users/deanpeters/ai-pm-exploration-toolkit/src/pm_audio_workflows.py --list

# Test 4: AI Chat Help
aipm chat --help
python3 /Users/deanpeters/ai-pm-exploration-toolkit/src/ai_chat.py --help

# WORKFLOW ORCHESTRATION TESTS
cd ~/temp
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh start n8n
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh status
sleep 45
curl -f http://localhost:5678 && echo "n8n UP" || echo "n8n DOWN"
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh start langflow
sleep 45
curl -f http://localhost:7860 && echo "langflow UP" || echo "langflow DOWN"
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh status

# WEB DASHBOARD TESTS
cd /Users/deanpeters/ai-pm-exploration-toolkit
python3 web/app.py &
WEB_PID=$!
sleep 10
curl -f http://localhost:3000 && echo "Web Dashboard UP" || echo "Web Dashboard DOWN"
kill $WEB_PID 2>/dev/null

# SYSTEM INTEGRATION TESTS
cd /Users/deanpeters/ai-pm-exploration-toolkit
./core/run_tests.sh --quick
./core/run_tests.sh --new-user

# GRACEFUL FAILURE TESTS
cd ~/temp
aipm data-gen --count=2 --type=b2b_saas --interactive
aipm research --type=company --company="MSFT" --detailed

# OUTPUT VERIFICATION
ls -la /Users/deanpeters/ai-pm-exploration-toolkit/outputs/personas/ | head -10
ls -la /Users/deanpeters/ai-pm-exploration-toolkit/outputs/research/ | head -10

# FULL SERVICE STACK
cd /Users/deanpeters/ai-pm-exploration-toolkit
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh start
sleep 60
python3 web/app.py &
WEB_PID=$!
sleep 10

# MANUAL BROWSER TESTING
open http://localhost:3000
open http://localhost:3000/tool/data-generation
open http://localhost:3000/tool/market-research
open http://localhost:3000/tool/ai-chat
open http://localhost:3000/tool/n8n-workflows
open http://localhost:3000/tool/audio-transcription
open http://localhost:5678
open http://localhost:7860

# CLEANUP
kill $WEB_PID 2>/dev/null
/Users/deanpeters/ai-pm-exploration-toolkit/workflows/orchestrate-workflows.sh stop