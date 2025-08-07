# AI PM Toolkit - Manual Testing Procedures 🛠️

## 📋 SYSTEMATIC MANUAL TESTING

This document provides **step-by-step procedures** for manual testing of every component in the AI PM Toolkit. Use these procedures to validate functionality when automated tests are insufficient or when testing user experience.

**Purpose:** Ensure every feature works from a human user perspective, not just from an automated testing perspective.

## 🎯 TESTING PHILOSOPHY

1. **Test Like a User** - Follow actual user workflows, not developer shortcuts
2. **Document Everything** - Record what you see, what works, what breaks
3. **Be Systematically Thorough** - Don't skip steps, even if they seem obvious
4. **Capture Evidence** - Screenshots, logs, and outputs for verification
5. **Test Edge Cases** - Try to break things intentionally

## 🧪 MANUAL TESTING SETUP

### Pre-Testing Environment Preparation

#### 1. Testing Environment Setup

```bash
# Create dedicated testing directory
mkdir -p ~/aipm-manual-testing
cd ~/aipm-manual-testing

# Create testing log file
echo "AI PM Toolkit Manual Testing Session - $(date)" > manual_test_log.txt
echo "================================================" >> manual_test_log.txt
```

#### 2. Browser Setup for Web Testing

**Required Browsers for Testing:**
- Chrome/Safari (primary)
- Firefox (secondary)  
- Mobile browser (responsive testing)

**Browser Configuration:**
1. Open Developer Console (F12)
2. Enable responsive design mode
3. Clear cache and cookies
4. Disable browser extensions (for clean testing)

#### 3. Audio Testing Setup

```bash
# Create test audio files for different scenarios
say "This is a test of user interview analysis. The user mentioned difficulty with the login process and requested a simpler authentication method." -o user_interview_test.wav

say "Team meeting summary test. We discussed quarterly goals, identified three key blockers, and assigned action items to resolve technical debt." -o meeting_summary_test.wav

say "Voice memo testing. Product feature idea: implement real-time collaboration in the dashboard for better team coordination." -o voice_memo_test.wav

echo "✅ Test audio files created" >> manual_test_log.txt
```

## 🏗️ INSTALLATION TESTING

### Procedure: Fresh Installation Validation

#### Step 1: Clean Environment Verification

**Manual Steps:**
1. Open new terminal window
2. Verify no aipm commands exist: `type aipm_dashboard`
   - **Expected:** `aipm_dashboard: command not found`
   - **Actual:** ________________
3. Check ports are free: `lsof -ti:3000,5678,7860,8082,8888`
   - **Expected:** No processes listed
   - **Actual:** ________________

**Record Results:**
```bash
echo "Clean environment check: [PASS/FAIL]" >> manual_test_log.txt
echo "Reason: ________________" >> manual_test_log.txt
```

#### Step 2: Repository Clone

**Manual Steps:**
1. Navigate to testing directory: `cd ~/aipm-manual-testing`
2. Clone repository: `git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git`
3. Enter directory: `cd ai-pm-exploration-toolkit`
4. List directory contents: `ls -la`
   - **Expected:** See core/, web/, src/, README.md, etc.
   - **Actual:** ________________

#### Step 3: CRITICAL Pre-Installation Service Shutdown

**⚠️  MANDATORY - DO NOT SKIP THIS STEP**

**Manual Steps:**
1. **Stop all services that could interfere:**
   ```bash
   echo "🛑 Stopping all services before installation..."
   
   # Kill processes on installer target ports
   sudo lsof -ti:3000 | xargs sudo kill -9 2>/dev/null || true
   sudo lsof -ti:5678 | xargs sudo kill -9 2>/dev/null || true
   sudo lsof -ti:7860 | xargs sudo kill -9 2>/dev/null || true
   sudo lsof -ti:8082 | xargs sudo kill -9 2>/dev/null || true
   sudo lsof -ti:8888 | xargs sudo kill -9 2>/dev/null || true
   
   # Stop Docker containers
   docker stop $(docker ps -aq) 2>/dev/null || true
   
   # Stop Ollama
   pkill ollama 2>/dev/null || true
   ```

2. **Verify ports are completely free:**
   ```bash
   echo "🔍 Verifying ports are free..."
   for port in 3000 5678 7860 8082 8888; do
       if lsof -ti:$port >/dev/null 2>&1; then
           echo "❌ CRITICAL: Port $port still occupied - installer will hang"
           lsof -ti:$port | xargs ps -p
           echo "Must kill before proceeding: sudo lsof -ti:$port | xargs sudo kill -9"
           exit 1
       else
           echo "✅ Port $port free"
       fi
   done
   ```

3. **Record pre-installation state:**
   - **All ports free:** ✅/❌
   - **Docker containers stopped:** ✅/❌
   - **Previous AIPM processes killed:** ✅/❌

**Why This Step Is Critical:**
- Prevents installer hanging for hours
- Prevents false "success" messages when services don't actually start
- Avoids port conflict errors that cause confusing failures

#### Step 4: Installer Execution

**Manual Steps:**
1. Run installer: `python3 core/installer.py`
2. **Watch for:**
   - Any Python errors or tracebacks
   - Progress messages
   - Success/failure indicators
   - Clear completion message
3. **Time the installation:** Start: _______ End: _______
   - **Expected:** < 5 minutes total time
   - **Actual Duration:** ________________

**Record Installer Output:**
```bash
python3 core/installer.py 2>&1 | tee installer_output.log
echo "Installer completion status: [SUCCESS/FAILED]" >> manual_test_log.txt
```

#### Step 4: Post-Installation Verification

**Manual Steps:**
1. Start new shell session: `exec $SHELL` or open new terminal
2. Test command availability:
   - `type aipm_dashboard` - **Expected:** Command definition shown
   - `type aipm_hub` - **Expected:** Command definition shown  
   - `type aipm_help` - **Expected:** Command definition shown
3. Test command execution:
   - `aipm_help` - **Expected:** Comprehensive help menu displayed
   - **Actual:** ________________

## 🌐 WEB DASHBOARD MANUAL TESTING

### Procedure: Web Interface Comprehensive Testing

#### Step 1: Dashboard Startup

**Manual Steps:**
1. Open terminal in project directory
2. Start dashboard: `aipm_dashboard`
3. **Observe startup messages:**
   - Flask development server messages
   - Port binding confirmation
   - No Python errors or warnings
   - **Expected:** "Running on http://localhost:3000"
   - **Actual:** ________________
4. **Keep terminal open** - Monitor for any runtime errors during testing

#### Step 2: Basic Web Access

**Manual Steps:**
1. Open browser to: `http://localhost:3000`
2. **Visual Inspection Checklist:**
   - [ ] Page loads without "Connection refused" error
   - [ ] "AI PM Toolkit" branding clearly visible
   - [ ] Navigation menu present
   - [ ] No broken images or missing CSS
   - [ ] Page layout looks professional
   - [ ] No browser console errors (check Developer Tools)

3. **Take Screenshot:** Save as `web_dashboard_main.png`

**Record Results:**
```bash
echo "Web dashboard basic access: [PASS/FAIL]" >> manual_test_log.txt
echo "Visual quality: [EXCELLENT/GOOD/POOR]" >> manual_test_log.txt
echo "Console errors: [NONE/MINOR/MAJOR]" >> manual_test_log.txt
```

#### Step 3: Authentication Testing

**Manual Steps:**
1. Look for login/authentication interface
2. **Test Guest Access (if available):**
   - Click "Guest" or "Continue without login"
   - **Expected:** Access to dashboard features
   - **Actual:** ________________

3. **Test User Registration (if available):**
   - Click "Register" or "Sign Up"
   - Fill form with test data
   - Submit registration
   - **Expected:** Successful registration or clear error messages
   - **Actual:** ________________

4. **Test Login Process:**
   - Use test credentials or guest access
   - **Expected:** Access to full dashboard
   - **Actual:** ________________

#### Step 4: Navigation Testing

**Manual Steps:**
1. **Test Each Menu Item:**
   - Audio Transcription Tool
   - AI Chat Interface
   - Market Research Tool
   - Data Generation Tool
   - Workflow Management
   - Any other menu items

2. **For Each Menu Item:**
   - Click the link
   - **Expected:** Page loads without 404 error
   - **Actual:** ________________
   - Verify page content is relevant to menu item
   - Check for broken functionality or missing elements
   - Take screenshot: `page_[menuitem].png`

**Record Results:**
```bash
echo "Navigation testing results:" >> manual_test_log.txt
echo "- Audio Transcription: [PASS/FAIL]" >> manual_test_log.txt  
echo "- AI Chat Interface: [PASS/FAIL]" >> manual_test_log.txt
echo "- Market Research: [PASS/FAIL]" >> manual_test_log.txt
# ... continue for all menu items
```

## 🎙️ AUDIO SYSTEM MANUAL TESTING

### Procedure: Audio Transcription Testing

#### Step 1: Audio System Status Check

**Manual Steps:**
1. Open terminal in project directory
2. Run: `python3 src/audio_transcription.py --status`
3. **Verify Status Output:**
   - "Whisper Available: ✅" should be displayed
   - List of available models shown
   - No Python import errors
   - **Actual Output:** ________________

#### Step 2: Web Interface Audio Upload

**Manual Steps:**
1. Navigate to Audio Transcription tool in web dashboard
2. **Test File Upload Interface:**
   - Verify drag & drop area is visible
   - Verify "Choose File" button works
   - **Expected:** Clear upload interface
   - **Actual:** ________________

3. **Upload Test Audio File:**
   - Drag `user_interview_test.wav` to upload area OR use file chooser
   - **Expected:** File upload progress indicator
   - **Actual:** ________________

4. **Configure Processing Options:**
   - Select appropriate model (turbo recommended for testing)
   - Choose use case: "User Interview Analysis"
   - Click "Process Audio" or equivalent button
   - **Expected:** Processing begins with progress indicator
   - **Actual:** ________________

5. **Monitor Processing:**
   - Watch for processing completion message
   - **Expected:** Results displayed on page within reasonable time
   - **Actual Processing Time:** _______ seconds
   - **Results Quality:** [EXCELLENT/GOOD/POOR]

#### Step 3: Command Line Audio Processing

**Manual Steps:**
1. Use command line for audio processing:
   ```bash
   python3 src/audio_transcription.py user_interview_test.wav --model turbo --use-case user_interviews
   ```

2. **Monitor Command Execution:**
   - Processing progress messages
   - Completion confirmation
   - Output file location
   - **Expected:** "✅ Transcription completed!"
   - **Actual:** ________________

3. **Verify Output Files:**
   - Check for created transcription files
   - Verify file contents are reasonable
   - **Expected:** Structured output with insights
   - **Actual File Location:** ________________

#### Step 4: PM Workflow Testing

**Manual Steps:**
1. Test PM workflow listing: `python3 src/pm_audio_workflows.py --list`
2. **Verify Workflow Availability:**
   - Count of available workflows (should be 6+)
   - Clear descriptions for each workflow
   - **Actual Workflow Count:** ________________

3. **Test Specific Workflow:**
   ```bash
   python3 src/pm_audio_workflows.py --workflow meeting_summary --audio meeting_summary_test.wav
   ```
   - **Expected:** Structured meeting analysis output
   - **Actual:** ________________

## 🤖 AI CHAT MANUAL TESTING

### Procedure: AI Chat System Testing

#### Step 1: AI Chat System Status

**Manual Steps:**
1. Check AI chat system: `python3 src/ai_chat.py --status`
2. **Verify Model Detection:**
   - List of available models displayed
   - Local models detected (if Ollama running)
   - Fallback options available
   - **Available Models:** ________________

#### Step 2: Web Interface Chat Testing

**Manual Steps:**
1. Navigate to AI Chat interface in web dashboard
2. **Test Chat Interface:**
   - Chat input box visible and functional
   - Model selection dropdown (if available)
   - Clear conversation history
   - **Interface Quality:** [EXCELLENT/GOOD/POOR]

3. **Test Chat Interaction:**
   - Type: "What are the key metrics for product managers?"
   - Click Send or press Enter
   - **Expected:** AI response within 30 seconds
   - **Actual Response Time:** _______ seconds
   - **Response Quality:** [RELEVANT/SOMEWHAT/IRRELEVANT]

4. **Test Follow-up Questions:**
   - Type: "How do I measure user engagement?"
   - Send message
   - **Expected:** Contextual response building on previous conversation
   - **Actual:** ________________

#### Step 3: Command Line Chat Testing

**Manual Steps:**
1. Test interactive chat mode:
   ```bash
   python3 src/ai_chat.py --mode pm_assistant --interactive
   ```

2. **Test Different Chat Modes:**
   - PM Assistant mode
   - Analysis mode
   - Brainstorming mode
   - **Functional Modes:** ________________

3. **Test Conversation Saving:**
   - Complete a short chat session
   - Exit with 'quit'
   - **Expected:** Conversation saved automatically
   - **Actual Save Location:** ________________

## 🐳 WORKFLOW SERVICES MANUAL TESTING

### Procedure: Docker Services Testing

#### Step 1: Workflow Service Startup

**Manual Steps:**
1. Start workflow services: `aipm_workflows`
2. **Monitor Startup Process:**
   - Docker container startup messages
   - Service initialization logs
   - Port binding confirmations
   - **Expected Startup Time:** < 2 minutes
   - **Actual Startup Time:** _______ minutes

3. **Check Service Status:**
   - Run: `aipm_workflows_status`
   - **Expected:** List of running services with ports
   - **Actual:** ________________

#### Step 2: Individual Service Testing

**Manual Steps for Each Service:**

**n8n Workflow Automation (Port 5678):**
1. Open browser to: `http://localhost:5678`
2. **Verify n8n Interface:**
   - [ ] Page loads without connection errors
   - [ ] n8n branding and interface visible
   - [ ] Can create new workflow
   - [ ] Basic nodes are draggable
3. **Take Screenshot:** `n8n_interface.png`

**Langflow AI Builder (Port 7860):**
1. Open browser to: `http://localhost:7860`
2. **Verify Langflow Interface:**
   - [ ] Page loads without errors
   - [ ] Langflow interface visible
   - [ ] Can create new flow
   - [ ] AI components available
3. **Take Screenshot:** `langflow_interface.png`

**Jupyter Lab (Port 8888):**
1. Open browser to: `http://localhost:8888`
2. **Verify Jupyter Interface:**
   - [ ] Jupyter Lab loads properly
   - [ ] File browser visible
   - [ ] Can create new notebook
   - [ ] Python kernel available
3. **Take Screenshot:** `jupyter_interface.png`

#### Step 3: Service Integration Testing

**Manual Steps:**
1. **Test Service Orchestration:**
   - Stop services: `aipm_workflows_stop`
   - **Expected:** All services stopped cleanly
   - **Actual:** ________________

2. **Test Service Restart:**
   - Start services: `aipm_workflows_start`
   - **Expected:** All services start successfully
   - **Actual:** ________________

3. **Test Service Status Monitoring:**
   - Check status: `aipm_workflows_status`
   - **Expected:** Accurate status of all services
   - **Actual:** ________________

## 🔗 INTEGRATION MANUAL TESTING

### Procedure: End-to-End Workflow Testing

#### Step 1: Complete User Journey Testing

**Scenario: PM User Interview Analysis**

**Manual Steps:**
1. **Start with Audio File:**
   - Upload `user_interview_test.wav` via web interface
   - Process through User Interview Analysis workflow
   - **Expected:** Structured insights about user pain points
   - **Actual Results:** ________________

2. **Follow with AI Analysis:**
   - Take transcription results to AI Chat
   - Ask: "Based on this user interview, what are the top 3 product improvements we should prioritize?"
   - **Expected:** Prioritized recommendations
   - **Actual AI Response:** ________________

3. **Document in Workflow Tool:**
   - Open n8n or ToolJet
   - Create simple workflow for tracking these insights
   - **Expected:** Functional workflow creation
   - **Actual:** ________________

#### Step 2: Cross-System Data Flow Testing

**Manual Steps:**
1. **Generate Synthetic Data:**
   - Use Data Generation tool to create 10 user personas
   - **Expected:** Realistic user data generated
   - **Actual:** ________________

2. **Analyze with AI Chat:**
   - Import generated data context into chat
   - Ask for market segmentation analysis
   - **Expected:** Strategic insights based on generated data
   - **Actual:** ________________

3. **Visualize in Workflow Tool:**
   - Create dashboard in ToolJet showing user segments
   - **Expected:** Functional data visualization
   - **Actual:** ________________

## 📊 DATA SYSTEMS MANUAL TESTING

### Procedure: Market Research & Data Generation Testing

#### Step 1: Market Research Testing

**Manual Steps:**
1. **Web Interface Testing:**
   - Navigate to Market Research tool
   - Enter test company: "Notion"
   - Select research type: "Competitive Analysis"
   - Submit request
   - **Expected:** Comprehensive company analysis
   - **Actual Results:** ________________

2. **Command Line Testing:**
   ```bash
   python3 src/market_research.py --company "Notion" --analysis competitive
   ```
   - **Expected:** Structured market intelligence
   - **Actual:** ________________

#### Step 2: Data Generation Testing

**Manual Steps:**
1. **Web Interface Testing:**
   - Navigate to Data Generation tool
   - Set parameters: 25 personas, B2B SaaS industry
   - Generate data
   - **Expected:** Realistic user personas with demographics, goals, pain points
   - **Actual Results Quality:** [EXCELLENT/GOOD/POOR]

2. **Command Line Testing:**
   ```bash
   python3 src/data_generator.py --personas 25 --industry saas --output synthetic_users.json
   ```
   - **Expected:** JSON file with structured persona data
   - **Actual File Size:** _______ KB

## 🚨 ERROR HANDLING MANUAL TESTING

### Procedure: Edge Cases and Error Scenarios

#### Step 1: Invalid Input Testing

**Manual Steps:**
1. **Audio System Error Handling:**
   - Try uploading non-audio file (e.g., .txt file)
   - **Expected:** Clear error message, graceful handling
   - **Actual:** ________________

2. **Web Interface Error Handling:**
   - Try accessing non-existent URL: `http://localhost:3000/nonexistent`
   - **Expected:** Friendly 404 page
   - **Actual:** ________________

3. **AI Chat Error Handling:**
   - Send extremely long message (>10,000 characters)
   - **Expected:** Appropriate length limit message
   - **Actual:** ________________

#### Step 2: Service Failure Testing

**Manual Steps:**
1. **Web Service Interruption:**
   - Kill web server process while using interface
   - Try to interact with page
   - **Expected:** Clear error message about connectivity
   - **Actual:** ________________

2. **Workflow Service Failure:**
   - Stop Docker while services running
   - Check service status
   - **Expected:** Accurate status reporting of failed services
   - **Actual:** ________________

## 📋 MANUAL TEST REPORT TEMPLATE

### Test Session Summary

**Date:** ________________  
**Tester:** ________________  
**Environment:** ________________  
**Version/Branch:** ________________  

### Test Results Overview

**Overall System Health:** [EXCELLENT/GOOD/FAIR/POOR]  
**User Experience Quality:** [EXCELLENT/GOOD/FAIR/POOR]  
**Performance:** [FAST/ACCEPTABLE/SLOW]  

### Component Test Results

| Component | Status | Issues | Notes |
|-----------|---------|---------|-------|
| Installation | ✅/❌ | | |
| Web Dashboard | ✅/❌ | | |
| Audio System | ✅/❌ | | |
| AI Chat | ✅/❌ | | |
| Workflow Services | ✅/❌ | | |
| Integration | ✅/❌ | | |

### Critical Issues Identified

**Blocking Issues (Must Fix Before Release):**
1. ________________
2. ________________

**Minor Issues (Can Address Later):**
1. ________________
2. ________________

### User Experience Assessment

**New User Experience:** [SMOOTH/ACCEPTABLE/FRUSTRATING]  
**Learning Curve:** [EASY/MODERATE/STEEP]  
**Documentation Accuracy:** [ACCURATE/MOSTLY/INACCURATE]  

### Recommendations

**Immediate Actions Required:**
1. ________________
2. ________________

**Future Improvements:**
1. ________________
2. ________________

### Evidence Collected

**Screenshots:** [List screenshot files]  
**Logs:** [List log files]  
**Test Files:** [List generated test files]  

### Sign-off

**Manual Testing Complete:** ✅  
**Ready for Release:** ✅/❌  
**Signature:** ________________  

---

## 🎯 TESTING BEST PRACTICES

### Before Starting Manual Testing

1. **Plan Your Session** - Allocate sufficient time (2-4 hours)
2. **Prepare Environment** - Clean testing setup
3. **Document Everything** - Screenshots, logs, observations
4. **Test Like a User** - Don't use developer shortcuts
5. **Test Edge Cases** - Try to break things intentionally

### During Testing

1. **Take Breaks** - Fresh eyes catch more issues
2. **Record Immediately** - Don't rely on memory
3. **Be Systematic** - Follow procedures completely
4. **Note Performance** - Record response times
5. **Test on Multiple Browsers** - Cross-browser compatibility

### After Testing

1. **Compile Evidence** - Organize screenshots and logs
2. **Prioritize Issues** - Critical vs. minor problems
3. **Write Clear Reports** - Actionable descriptions
4. **Share Findings** - Communicate with development team
5. **Update Procedures** - Improve testing based on learnings

---

## 💡 CONCLUSION

Manual testing is essential for validating user experience beyond what automated tests can verify. These procedures ensure that the AI PM Toolkit actually works from a human user perspective.

**Key Principles:**
- Test systematically and thoroughly
- Document everything with evidence
- Focus on user experience quality
- Don't skip edge cases and error scenarios
- Provide actionable feedback for improvements

Use these procedures regularly, especially before releases, to maintain high quality and prevent user frustration.

---
*🛠️ Manual Testing Procedures - Because humans see what machines miss*