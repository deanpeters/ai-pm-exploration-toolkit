#!/bin/bash

# AI PM Toolkit - Quick Test Runner
# Automated test script for contributors

set -e  # Exit on any error

echo "🧪 AI PM Toolkit - Contributors Test Runner"
echo "=========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper functions
log_test() {
    echo -n "🧪 Testing: $1 ... "
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

log_pass() {
    echo -e "${GREEN}✅ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
}

log_fail() {
    echo -e "${RED}❌ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    if [ ! -z "$1" ]; then
        echo "   Error: $1"
    fi
}

log_skip() {
    echo -e "${YELLOW}⏭️  SKIP${NC}"
    if [ ! -z "$1" ]; then
        echo "   Reason: $1"
    fi
}

# Parse command line arguments
QUICK_ONLY=false
SKIP_MANUAL=true
VERBOSE=false
NEW_USER_TEST=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_ONLY=true
            shift
            ;;
        --full)
            SKIP_MANUAL=false
            shift
            ;;
        --new-user)
            NEW_USER_TEST=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --quick     Run only quick tests (default)"
            echo "  --full      Run full test suite including manual tests"
            echo "  --new-user  Run first-time user experience test"
            echo "  --verbose   Show detailed output"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo "Test Mode: $([ "$NEW_USER_TEST" = true ] && echo "New User Experience Test" || ([ "$QUICK_ONLY" = true ] && echo "Quick Tests Only" || echo "Full Test Suite"))"
echo

# Check prerequisites
echo "📋 Checking Prerequisites"
echo "-------------------------"

log_test "Python 3 availability"
if python3 --version >/dev/null 2>&1; then
    log_pass
else
    log_fail "Python 3 not found"
fi

log_test "Required Python packages"
if python3 -c "import requests, flask, pathlib" >/dev/null 2>&1; then
    log_pass
else
    log_fail "Missing required packages. Run: pip3 install requests flask pathlib"
fi

log_test "Repository structure"
if [[ -d "src" && -d "web" && -d "core" && -d "outputs" ]]; then
    log_pass
else
    log_fail "Missing required directories. Are you in the project root?"
fi

echo

# New User Experience Test
if [ "$NEW_USER_TEST" = true ]; then
    echo "👥 New User Experience Test"
    echo "---------------------------"
    echo
    
    log_test "Fresh installation simulation"
    # Create temporary directory for clean test
    TEST_DIR="/tmp/aipm-new-user-test-$(date +%s)"
    if git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git "$TEST_DIR" >/dev/null 2>&1; then
        cd "$TEST_DIR"
        if python3 core/installer.py >/dev/null 2>&1; then
            log_pass
        else
            log_fail "Installation failed for new user"
        fi
        cd - >/dev/null
        rm -rf "$TEST_DIR" 2>/dev/null
    else
        log_fail "Could not clone repository for new user test"
    fi
    
    log_test "5-minute quick win - Audio transcription ready"
    if python3 src/audio_transcription.py --status 2>/dev/null | grep -q "Whisper Available: ✅"; then
        log_pass
    else
        log_fail "Audio transcription not immediately available"
    fi
    
    log_test "Web dashboard immediate access"
    python3 web/app.py &
    WEB_PID=$!
    sleep 5
    if curl -s http://localhost:3000 2>/dev/null | grep -q "AI PM Toolkit"; then
        log_pass
        echo "   Dashboard available at: http://localhost:3000"
    else
        log_fail "Web dashboard not accessible to new users"
    fi
    kill $WEB_PID 2>/dev/null || true
    
    log_test "Clear learning path documentation"
    if [[ -f "README.md" && -f "CLAUDE.md" ]]; then
        log_pass
        echo "   New users have clear documentation path"
    else
        log_fail "Missing essential documentation for new users"
    fi
    
    log_test "Helpful error messages for new users"
    if python3 src/audio_transcription.py nonexistent.wav 2>&1 | grep -qi "error\|help\|try"; then
        log_pass
        echo "   Error messages guide users constructively"
    else
        log_fail "Error messages not helpful for new users"
    fi
    
    echo
    echo "🎯 New User Success Summary:"
    echo "- Users should achieve success in < 5 minutes"
    echo "- Clear value demonstration with audio transcription"
    echo "- Web dashboard works without configuration"
    echo "- Helpful guidance when things go wrong"
    echo
fi

# Skip core component tests if only running new user test
if [ "$NEW_USER_TEST" = true ]; then
    echo "New User Experience Test Complete!"
    echo
    echo "📊 Test Summary"
    echo "==============="
    echo -e "Total Tests: $TOTAL_TESTS"
    echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo
        echo -e "${GREEN}🎉 New User Experience Test Passed!${NC}"
        echo "The toolkit provides a good first-time user experience."
        exit 0
    else
        echo
        echo -e "${RED}❌ New User Experience needs improvement.${NC}"
        echo "Please address the failing tests to improve user onboarding."
        exit 1
    fi
fi

# Core Component Tests (Intuitive order: Web → CLI → Technical)
echo "🔧 Core Component Tests"
echo "-----------------------"
echo "Testing in user experience order: most approachable to most technical"
echo

# Test 1: Web Dashboard System (Most approachable first)
log_test "Web app imports"
if python3 -c "from web.app import app; print('Flask app imported')" >/dev/null 2>&1; then
    log_pass
else
    log_fail "Web app import failed"
fi

log_test "Web server basic startup"
python3 web/app.py &
WEB_PID=$!
sleep 3
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    log_pass
    echo "   Web dashboard accessible at http://localhost:3000"
else
    log_fail "Web server not responding"
fi
kill $WEB_PID 2>/dev/null || true

# Test 2: CLI Commands (User-facing tools second)
log_test "CLI command availability check"
# Check if some key commands exist (may not be available in test environment)
if [[ -n "$(type aipm_transcribe 2>/dev/null)" ]] || [[ -f "cli/tools/audio_transcription.py" ]]; then
    log_pass
    echo "   CLI tools available or accessible"
else
    log_skip "CLI commands not installed (run installer.py first)"
fi

# Test 3: Audio Intelligence System (Core AI value third)
log_test "Audio transcription imports"
if python3 -c "import sys; sys.path.append('src'); from audio_transcription import AudioTranscriptionEngine; print('Import successful')" >/dev/null 2>&1; then
    log_pass
else
    log_fail "Audio transcription import failed"
fi

log_test "Whisper availability"
if python3 src/audio_transcription.py --status 2>/dev/null | grep -q "Whisper Available: ✅"; then
    log_pass
else
    log_fail "Whisper not available or status check failed"
fi

log_test "PM audio workflows"
if python3 src/pm_audio_workflows.py --list 2>/dev/null | grep -q "Available PM Audio Workflows"; then
    log_pass
else
    log_fail "PM workflows not working"
fi

# Test 4: AI Chat System (Requires technical setup)  
log_test "AI chat system imports"
if python3 -c "import sys; sys.path.append('src'); from ai_chat import AIChat; print('Import successful')" >/dev/null 2>&1; then
    log_pass
else
    log_fail "AI chat import failed"
fi

log_test "AI chat model detection"
if python3 -c "import sys; sys.path.append('src'); from ai_chat import AIChat; chat = AIChat('.'); models = chat._detect_available_models(); print(f'Models detected: {sum(models.values())}')" 2>/dev/null | grep -q "Models detected:"; then
    log_pass
else
    log_fail "AI model detection failed"
fi

# Test 5: Workflow Orchestration (Docker setup)
log_test "Workflow orchestration script"
if [[ -x "workflows/orchestrate-workflows.sh" ]] || [[ -f "orchestrate-workflows.sh" ]]; then
    log_pass
    echo "   Docker workflow tools available"
else
    log_skip "Docker workflow scripts not executable"
fi

# Test 6: Data Integration (Backend components)
log_test "Market research system"
if python3 -c "import sys; sys.path.append('src'); from market_research import research_company_data; print('Market research ready')" >/dev/null 2>&1; then
    log_pass
else
    log_fail "Market research import failed"
fi

# Test 7: Goose Integration (Most technical)
log_test "Goose integration"
if python3 src/goose_integration.py --status 2>/dev/null | grep -q "Goose CLI Integration Status"; then
    log_pass
else
    log_fail "Goose integration not working"
fi

echo

# Integration Tests (only if not quick-only mode)
if [ "$QUICK_ONLY" = false ]; then
    echo "🔗 Integration Tests"
    echo "-------------------"

    # Test web server startup
    log_test "Web server startup"
    if python3 web/app.py &
    then
        WEB_PID=$!
        sleep 5
        
        if curl -s http://localhost:3000/api/status >/dev/null 2>&1; then
            log_pass
            kill $WEB_PID 2>/dev/null || true
        else
            log_fail "Web server not responding"
            kill $WEB_PID 2>/dev/null || true
        fi
    else
        log_fail "Could not start web server"
    fi

    # Test workflow orchestration
    log_test "Workflow orchestration script"
    if [[ -x "workflows/orchestrate-workflows.sh" ]]; then
        if ./workflows/orchestrate-workflows.sh status >/dev/null 2>&1; then
            log_pass
        else
            log_fail "Workflow orchestration failed"
        fi
    else
        log_skip "Orchestration script not executable"
    fi

    echo
fi

# Manual Tests Reminder
if [ "$SKIP_MANUAL" = true ]; then
    echo "⚠️  Manual Tests Skipped"
    echo "------------------------"
    echo "For complete validation, also test manually:"
    echo "  • Audio file transcription with real MP3/WAV"
    echo "  • Interactive AI chat session"
    echo "  • Web dashboard navigation"
    echo "Run with --full flag to include integration tests"
    echo
fi

# Summary
echo "📊 Test Summary"
echo "==============="
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo
    echo -e "${GREEN}🎉 All tests passed! Your changes are ready for submission.${NC}"
    echo
    echo "Next steps:"
    echo "  1. Run any relevant manual tests"
    echo "  2. Update documentation if needed"
    echo "  3. Create your pull request"
    exit 0
else
    echo
    echo -e "${RED}❌ Some tests failed. Please fix issues before submitting.${NC}"
    echo
    echo "Troubleshooting:"
    echo "  1. Check error messages above"
    echo "  2. Review CONTRIBUTORS_TEST_PLAN.md for detailed debugging"
    echo "  3. Ensure all dependencies are installed"
    echo "  4. Verify you're running from project root directory"
    exit 1
fi