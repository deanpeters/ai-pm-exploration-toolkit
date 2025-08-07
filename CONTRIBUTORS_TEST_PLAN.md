# AI PM Toolkit - Contributors Test Plan 🧪

## Overview
This test plan ensures all core components work correctly before submitting code changes to GitHub. It's designed to catch integration issues, validate new features, and maintain the quality of the AI PM Exploration Toolkit.

**Target Audience**: Contributors, maintainers, and anyone making changes to the codebase.

## 🚨 **PRE-REQUISITES**

Before running any tests, ensure your environment is properly configured:

### **System Requirements**
```bash
# Verify Python 3.8+ is installed
python3 --version

# Verify required packages are installed
pip3 install openai-whisper requests flask pathlib

# Verify Docker is running (for workflow tests)
docker --version && docker info

# Verify Ollama is running (for AI chat tests)
curl -s http://localhost:11434/api/tags
```

### **Repository Setup**
```bash
# Clone and navigate to repository
git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git
cd ai-pm-exploration-toolkit

# Verify directory structure
ls -la shared/ web/ cli/ transcripts/ 

# Load environment (if using installer)
source ~/.zshrc  # or ~/.bashrc
```

## 🧪 **CORE COMPONENT TESTS**

### **1. Web Dashboard System Test** 🌐
**Critical Path**: Flask app, authentication, API endpoints, and web interface
**Why First**: Most approachable, visual, immediate value for users

#### **Test 1.1: Web Server Startup**
```bash
# Start web server (run in background or separate terminal)
python3 web/app.py &
WEB_PID=$!

# Wait for startup
sleep 5

# Test basic connectivity
curl -s http://localhost:3000 | grep -q "AI PM Toolkit" && echo "✅ Web server running" || echo "❌ Web server failed"

# Kill web server
kill $WEB_PID 2>/dev/null
```
**❌ FAIL CRITERIA**: Server won't start, connection refused, or missing templates

#### **Test 1.2: Web Interface Access** ⚠️ **MANUAL TEST**
```bash
# Start web server
python3 web/app.py &
WEB_PID=$!
sleep 5

# Open browser to http://localhost:3000
# User should see:
# • Clear AI PM Toolkit interface
# • Navigation menu with tools
# • Audio transcription upload area
# • Status indicators

echo "✅ Manual check: Web interface should be user-friendly and functional"

kill $WEB_PID 2>/dev/null
```
**❌ FAIL CRITERIA**: Interface not accessible, broken layout, or missing functionality

#### **Test 1.3: Authentication System**
```bash
# Test authentication status endpoint
python3 web/app.py &
WEB_PID=$!
sleep 5

curl -s http://localhost:3000/api/auth/status | python3 -m json.tool

# Expected Output: JSON with authentication status

kill $WEB_PID 2>/dev/null
```
**❌ FAIL CRITERIA**: API returns errors, authentication system broken, or JSON malformed

#### **Test 1.4: Web Audio Processing** ⚠️ **MANUAL TEST**
```bash
# Start web server
python3 web/app.py &
WEB_PID=$!
sleep 5

echo "✅ Manual check: Upload audio file through web interface"
echo "   • Navigate to audio transcription tool"
echo "   • Drag and drop MP3/WAV file"
echo "   • Verify processing works"
echo "   • Check results display correctly"

kill $WEB_PID 2>/dev/null
```

### **2. CLI Commands Test** 💻
**Critical Path**: Command aliases, user-friendly tools
**Why Second**: User-facing tools that provide immediate value

#### **Test 2.1: CLI Command Availability**
```bash
# Test if installer created proper aliases
# Note: This requires running the installer first

# Test key commands exist in current environment
type aipm_transcribe 2>/dev/null && echo "✅ aipm_transcribe available" || echo "❌ aipm_transcribe missing"
type aipm_audio_workflows 2>/dev/null && echo "✅ aipm_audio_workflows available" || echo "❌ aipm_audio_workflows missing"
type aipm_chat 2>/dev/null && echo "✅ aipm_chat available" || echo "❌ aipm_chat missing"
```
**❌ FAIL CRITERIA**: Commands missing, not executable, or not in PATH

#### **Test 2.2: CLI Command Execution**
```bash
# Test command execution
aipm_audio_workflows | grep -q "Available PM Audio Workflows" && echo "✅ Workflow listing works" || echo "❌ Workflow listing failed"

# Test audio transcription status
aipm_transcribe --help | grep -q "usage" && echo "✅ Audio CLI help works" || echo "❌ Audio CLI help failed"
```
**❌ FAIL CRITERIA**: Commands don't execute, error messages, or missing functionality

### **3. Audio Intelligence System Test** 🎙️
**Critical Path**: Whisper integration, PM workflows, transcription engine
**Why Third**: Technical but user-focused, demonstrates core AI value

#### **Test 3.1: Basic Transcription Status**
```bash
# Test Whisper availability
python3 shared/audio_transcription.py --status

# Expected Output:
# 🎙️ Audio Transcription Status
# ========================================
# Whisper Available: ✅
# Default Model: turbo
# Available Models: [list of 5 models]
```
**❌ FAIL CRITERIA**: Whisper not available, missing models, or import errors

#### **Test 3.2: PM Workflow Templates**
```bash
# Test workflow listing
python3 shared/pm_audio_workflows.py --list

# Expected Output:
# 🎯 Available PM Audio Workflows
# [6 workflow templates with descriptions]
```
**❌ FAIL CRITERIA**: Missing workflows, import errors, or incomplete descriptions

#### **Test 3.3: Audio File Processing** ⚠️ **MANUAL TEST**
```bash
# Create test audio file (record 10-second voice memo saying "This is a test for the AI PM toolkit audio transcription system")
# OR use any existing MP3/WAV file

# Test basic transcription
python3 shared/audio_transcription.py test_audio.mp3 --model turbo --use-case voice_memos

# Expected Output:
# ✅ Transcription completed!
# [Processing details, text preview, file paths]
```
**❌ FAIL CRITERIA**: Transcription fails, no output files created, or processing errors

### **4. AI Chat System Test** 🤖
**Critical Path**: Model detection, chat functionality, integration
**Why Fourth**: User-facing but requires technical setup (Ollama)

#### **Test 4.1: Model Detection**
```bash
# Test AI chat model detection
python3 shared/ai_chat.py --mode analysis --model ollama --dir .

# Expected Output:
# Available models: [list including qwen2.5, deepseek-r1, llama3.2]
```
**❌ FAIL CRITERIA**: No models detected, Ollama connection fails, or import errors

#### **Test 4.2: Chat Functionality** ⚠️ **MANUAL TEST**
```bash
# Test interactive chat (exit quickly with 'quit')
python3 shared/ai_chat.py --mode pm_assistant --interactive --dir .

# Type: "What are key PM metrics?"
# Type: "quit"

# Expected Output:
# [AI response about PM metrics, conversation saved]
```
**❌ FAIL CRITERIA**: No AI response, connection errors, or conversation not saved

### **5. Workflow Orchestration Test** 🐳
**Critical Path**: Docker containers, service management
**Why Fifth**: More technical setup, requires Docker

#### **Test 5.1: Docker System Check**
```bash
# Test Docker orchestration script
chmod +x workflow-tools/orchestrate-workflows.sh
./workflow-tools/orchestrate-workflows.sh status

# Expected Output:
# [Status of n8n, langflow, and other services]
```
**❌ FAIL CRITERIA**: Script not executable, Docker errors, or service status failures

#### **Test 5.2: Service Startup Test** ⚠️ **MANUAL TEST - OPTIONAL**
```bash
# Test starting essential services (n8n + langflow)
# WARNING: This will start Docker containers
./workflow-tools/orchestrate-workflows.sh start

# Wait for startup
sleep 30

# Check services
./workflow-tools/orchestrate-workflows.sh status

# Cleanup
./workflow-tools/orchestrate-workflows.sh stop
```
**❌ FAIL CRITERIA**: Services won't start, port conflicts, or containers fail

### **6. Data Integration Test** 📊
**Critical Path**: Market research, data generation
**Why Sixth**: Backend technical components

#### **Test 6.1: Market Research Engine**
```bash
# Test market research availability
python3 shared/market_research.py --help

# Expected Output: Help text with available commands
```
**❌ FAIL CRITERIA**: Import errors, missing dependencies, or help not displayed

#### **Test 6.2: Data Generator**
```bash
# Test synthetic data generation
python3 shared/data_generator.py --help

# Expected Output: Help text for data generation options
```
**❌ FAIL CRITERIA**: Import errors or missing functionality

### **7. Goose Integration Test** 🦢
**Critical Path**: Goose CLI integration and configuration
**Why Last**: Developer tools, most technical setup

#### **Test 7.1: Goose Integration Status**
```bash
# Test Goose integration
python3 shared/goose_integration.py --status

# Expected Output:
# 🦢 Goose CLI Integration Status
# [Status details with available models]
```
**❌ FAIL CRITERIA**: Goose not found, configuration errors, or missing models

## 🔍 **INTEGRATION TESTS**

### **Integration Test 1: End-to-End Audio Processing**
**Goal**: Test complete audio transcription workflow

```bash
# Create test audio file (or use existing one)
echo "Testing end-to-end audio processing workflow"

# Test workflow execution
python3 shared/pm_audio_workflows.py --workflow voice_memo_processing --audio test_audio.mp3 --output test_results.json

# Verify output files created
ls -la transcripts/voice_memos/ | head -5
cat test_results.json | python3 -m json.tool | head -20
```

**✅ PASS CRITERIA**: 
- Audio processed successfully
- Output files created in correct directories  
- JSON results contain expected structure
- No error messages during processing

### **Integration Test 2: Web-to-Backend Communication**
**Goal**: Test API endpoints and data flow

```bash
# Start web server
python3 web/app.py &
WEB_PID=$!
sleep 5

# Test API endpoints
echo "Testing API endpoints..."

# Test status endpoint
curl -s http://localhost:3000/api/status | python3 -m json.tool

# Test auth status
curl -s http://localhost:3000/api/auth/status | python3 -m json.tool

# Test AI chat status
curl -s -X POST -H "Content-Type: application/json" -d '{"action":"status"}' http://localhost:3000/api/ai-chat | python3 -m json.tool

kill $WEB_PID 2>/dev/null
```

**✅ PASS CRITERIA**:
- All API endpoints return valid JSON
- Status endpoints show system availability
- No 500 errors or connection failures

### **Integration Test 3: CLI Command Integration**
**Goal**: Test command aliases and integration

```bash
# Test if installer created proper aliases
# Note: This requires running the installer first

# Test key commands exist in current environment
type aipm_transcribe 2>/dev/null && echo "✅ aipm_transcribe available" || echo "❌ aipm_transcribe missing"
type aipm_audio_workflows 2>/dev/null && echo "✅ aipm_audio_workflows available" || echo "❌ aipm_audio_workflows missing"

# Test command execution
aipm_audio_workflows | grep -q "Available PM Audio Workflows" && echo "✅ Workflow listing works" || echo "❌ Workflow listing failed"
```

**✅ PASS CRITERIA**:
- All aipm_* commands available
- Commands execute without errors
- Expected output format returned

## 🚨 **CRITICAL FAILURE TESTS**

### **Failure Test 1: Missing Dependencies**
**Goal**: Ensure graceful handling of missing components

```bash
# Test behavior when Whisper is not available
# Temporarily rename whisper command
which whisper > /dev/null && sudo mv $(which whisper) $(which whisper).backup 2>/dev/null

# Test transcription status
python3 shared/audio_transcription.py --status

# Expected: Should show "Whisper not available" with install instructions

# Restore whisper if backed up
sudo mv $(which whisper).backup $(which whisper) 2>/dev/null || true
```

### **Failure Test 2: Invalid Audio Files**
```bash
# Test with invalid audio file
echo "This is not an audio file" > fake_audio.txt

python3 shared/audio_transcription.py fake_audio.txt --status

# Expected: Should fail gracefully with clear error message

rm fake_audio.txt
```

### **Failure Test 3: Network/Service Failures**
```bash
# Test behavior when Ollama is not running
# Stop Ollama temporarily if running
pkill ollama 2>/dev/null || true
sleep 2

python3 shared/ai_chat.py --status

# Expected: Should show fallback to mock responses

# Restart Ollama if it was running
ollama serve > /dev/null 2>&1 &
```

## 👥 **FIRST-TIME USER EXPERIENCE TEST**

**Critical Test**: Validate that new users can install and succeed quickly without becoming contributors.

### **User Profile**: New PM who wants to try the toolkit (5-minute quick win)

```bash
# Simulate fresh environment - Test this on a clean machine or VM
# This represents a PM who heard about the toolkit and wants to try it

echo "🎯 Testing First-Time User Experience"
echo "======================================="
echo

# Test 1: Clean installation from scratch
echo "1. Testing Clean Installation..."

# Clone repository (simulate fresh user)
git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git test-user-install
cd test-user-install

# Run installer as first-time user would
python3 installer.py

# Verify user gets success message and clear next steps
echo "✅ Installation completed - user should see clear next steps"

# Test 2: Immediate value demonstration (5-minute win)
echo
echo "2. Testing Immediate Value (5-minute win)..."

# Test the simplest, most impressive feature first
echo "Testing simplest workflow - audio transcription..."

# User should be able to:
# A) Record a 30-second voice memo saying "This is a test of the AI PM toolkit"
# B) Process it immediately
echo "Record test audio: 'This is a test of the AI PM toolkit. I want to see if this works quickly and easily.'"

# Test with built-in sample or user recording
python3 shared/audio_transcription.py --status | grep -q "Whisper Available: ✅" && echo "✅ Audio ready for immediate use"

# Test 3: Web dashboard immediate access
echo
echo "3. Testing Web Dashboard Quick Access..."

# Start dashboard
python3 web/app.py &
WEB_PID=$!
sleep 5

# User should see working dashboard immediately
curl -s http://localhost:3000 | grep -q "AI PM Toolkit" && echo "✅ Web dashboard accessible to new users"

echo "Dashboard should be available at: http://localhost:3000"
echo "New user should see clear interface with quick-start options"

kill $WEB_PID 2>/dev/null

# Test 4: Learning path clarity
echo
echo "4. Testing Learning Path Clarity..."

# Check if user has clear next steps
echo "Testing if new user has clear next steps:"
echo "• Documentation should explain what to do next"
echo "• Examples should be immediately runnable"  
echo "• User should understand value proposition"

ls -la README.md PHASE*.md *.md | head -5 && echo "✅ Documentation available for learning"

# Test 5: Quick failure recovery
echo
echo "5. Testing Error Recovery for New Users..."

# Test what happens when something goes wrong
echo "Testing graceful failure handling:"
python3 shared/audio_transcription.py nonexistent.wav 2>&1 | grep -i "error\|help\|try" && echo "✅ Helpful error messages for new users"

echo
echo "📊 First-Time User Experience Results:"
echo "======================================"
echo "✅ Installation should complete without errors"
echo "✅ User should achieve success in < 5 minutes" 
echo "✅ Web dashboard should be immediately accessible"
echo "✅ Clear next steps should be provided"
echo "✅ Error messages should guide users, not confuse them"
echo
echo "🎯 New User Success Criteria:"
echo "• Can install and see working demo in 5 minutes"
echo "• Understands value proposition immediately"
echo "• Has clear path to learn more without contribution pressure"
echo "• Gets helpful guidance when things go wrong"

# Cleanup test directory
cd ..
rm -rf test-user-install 2>/dev/null || true
```

**❌ NEW USER FAIL CRITERIA:**
- Installation takes > 5 minutes or fails
- No immediate working example  
- Confusing error messages
- Unclear value demonstration
- No obvious next steps for learning

**✅ NEW USER PASS CRITERIA:**
- **5-minute success**: User sees working AI transcription
- **Clear value**: Understands PM benefit immediately
- **Easy access**: Web dashboard works without configuration
- **Learning path**: Obvious next steps without contributor pressure
- **Error recovery**: Helpful messages guide user to success

---

## 📋 **PRE-COMMIT CHECKLIST**

Before submitting any changes to GitHub, run this complete test sequence:

### **Quick Tests (5 minutes)**
```bash
# Use automated test runner
./run_tests.sh --quick

# OR manually run core tests:

# 1. Verify core imports work
python3 -c "from shared.audio_transcription import AudioTranscriptionEngine; print('✅ Audio transcription imports')"
python3 -c "from shared.ai_chat import AIChat; print('✅ AI chat imports')" 
python3 -c "from shared.market_research import research_company_data; print('✅ Market research imports')"

# 2. Test basic functionality
python3 shared/audio_transcription.py --status | grep -q "Whisper Available: ✅" && echo "✅ Whisper ready"
python3 shared/pm_audio_workflows.py --list | grep -q "Available PM Audio Workflows" && echo "✅ Workflows ready"

# 3. Test web server startup
python3 web/app.py &
WEB_PID=$!
sleep 5
curl -s http://localhost:3000/api/status | grep -q "running" && echo "✅ Web server ready"
kill $WEB_PID 2>/dev/null
```

### **New User Experience Test (5 minutes)**
```bash
# Test first-time user install and success
./run_tests.sh --new-user

# This validates:
# • Clean installation works
# • 5-minute quick win achievable
# • Web dashboard immediately accessible  
# • Clear learning path provided
# • Helpful error recovery
```

### **Full Tests (15-30 minutes)** ⚠️ **REQUIRED FOR MAJOR CHANGES**
```bash
# Run all core component tests from sections 1-6 above
# Run all integration tests
# Run critical failure tests
# Verify no regression in existing functionality
```

## 🎯 **TESTING DIFFERENT CHANGE TYPES**

### **Web Dashboard Changes** 🌐  
- Run Web Dashboard System Tests (Section 1)
- Run Integration Test 2 (Web-to-Backend Communication)
- Test authentication flows manually
- Manual web interface navigation testing

### **CLI/Installer Changes** 💻
- Run CLI Commands Tests (Section 2)
- Run Integration Test 3 (CLI Command Integration)
- Test installer script on clean environment
- Verify all aipm_* commands work

### **Audio System Changes** 🎙️
- Run Audio Intelligence System Tests (Section 3)
- Run Integration Test 1 (End-to-End Audio Processing)
- Test with multiple audio formats (MP3, WAV, M4A)

### **AI Chat Changes** 🤖
- Run AI Chat System Tests (Section 4)
- Test different chat modes (pm_assistant, analysis, brainstorm)
- Verify model selection logic

### **Workflow/Docker Changes** 🐳
- Run Workflow Orchestration Tests (Section 5)
- Test service startup/shutdown cycles
- Verify container networking

### **Data Integration Changes** 📊
- Run Data Integration Tests (Section 6)  
- Test market research functionality
- Verify data generation capabilities

### **Goose/Developer Tool Changes** 🦢
- Run Goose Integration Tests (Section 7)
- Test CLI integration and configuration
- Verify model availability and status

## 🔧 **DEBUGGING FAILED TESTS**

### **Common Issues and Solutions**

#### **"Import Error" or "Module Not Found"**
```bash
# Check Python path
echo $PYTHONPATH

# Verify shared modules accessible
ls -la shared/
python3 -c "import sys; print('\n'.join(sys.path))"

# Fix: Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/shared"
```

#### **"Whisper Not Available"**
```bash
# Check Whisper installation
whisper --help

# Reinstall if needed
pip3 install openai-whisper

# Check PATH
echo $PATH | grep -q pip && echo "pip in PATH" || echo "pip PATH issue"
```

#### **"Ollama Connection Failed"**
```bash
# Check if Ollama is running
curl -s http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve &

# Check available models
ollama list
```

#### **"Web Server Won't Start"**
```bash
# Check port availability
lsof -ti:3000 | xargs kill 2>/dev/null || true

# Check Flask installation
python3 -c "import flask; print(f'Flask version: {flask.__version__}')"

# Check template directory
ls -la web/templates/
```

#### **"Docker/Workflow Issues"**
```bash
# Check Docker status
docker info

# Clean up containers
docker system prune -f

# Check script permissions
chmod +x workflow-tools/*.sh
```

## 📊 **TEST RESULTS DOCUMENTATION**

When submitting changes, include test results in your PR description:

```markdown
## Test Results

### Quick Tests
- [x] ✅ Core imports working
- [x] ✅ Whisper availability confirmed  
- [x] ✅ Web server startup successful

### Component Tests  
- [x] ✅ Audio Intelligence System (3/3 tests passed)
- [x] ✅ AI Chat System (2/2 tests passed)  
- [x] ✅ Web Dashboard System (2/2 tests passed)
- [x] ✅ [Additional components tested]

### Integration Tests
- [x] ✅ End-to-End Audio Processing
- [x] ✅ Web-to-Backend Communication  
- [x] ✅ CLI Command Integration

### Manual Tests Completed
- [x] Audio file transcription with real MP3
- [x] Interactive AI chat session
- [x] Web dashboard navigation

### Known Issues
- [ ] [List any issues discovered during testing]
- [ ] [Include workarounds or planned fixes]
```

## 🚀 **PERFORMANCE BENCHMARKS**

For performance-related changes, include these benchmarks:

### **Audio Processing Benchmarks**
```bash
# Test audio processing speed
time python3 shared/audio_transcription.py test_audio.mp3 --model turbo

# Expected: < 2x real-time for turbo model
# Example: 30-second audio should process in < 60 seconds
```

### **Web Response Benchmarks**
```bash
# Test API response times
time curl -s http://localhost:3000/api/status

# Expected: < 500ms for status endpoints
# Expected: < 2s for AI chat responses  
```

## ✅ **SIGN-OFF CRITERIA**

Before marking your changes as ready for review:

- [ ] **All Quick Tests Pass** (5-minute test suite)
- [ ] **Relevant Component Tests Pass** (based on change type)
- [ ] **At Least One Integration Test Passes** (end-to-end verification)
- [ ] **Manual Testing Completed** (for UI/UX changes)
- [ ] **No New Errors in Logs** (clean execution)
- [ ] **Documentation Updated** (if new features added)
- [ ] **Test Results Documented** (in PR description)

## 📞 **GETTING HELP**

If tests are failing and you can't resolve the issues:

1. **Check the troubleshooting section** in this document
2. **Review error logs** for specific error messages  
3. **Test on clean environment** to isolate the issue
4. **Document the failure** with steps to reproduce
5. **Create an issue** on GitHub with test failure details

## 🎯 **CONCLUSION**

This test plan ensures that:
- **Core functionality works** across all major components
- **Integration points are validated** before code submission
- **Regressions are caught early** in the development process
- **Contributors have confidence** their changes won't break existing features

**Remember**: It's better to catch issues during testing than after they're in production. Take time to run appropriate tests based on the scope of your changes.

**Happy Contributing!** 🚀

---
*This test plan is a living document. Update it as new components are added or testing procedures change.*