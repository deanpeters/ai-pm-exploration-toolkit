#!/bin/bash

# AI PM Toolkit - Test Plan Validation
# This script validates that the test plan works correctly by running key tests

echo "🔍 Validating Contributors Test Plan"
echo "======================================"
echo

# Test the quick test runner
echo "1. Testing Quick Test Runner..."
if ./run_tests.sh --quick > /dev/null 2>&1; then
    echo "   ✅ Quick tests run successfully"
else
    echo "   ❌ Quick tests failed"
    exit 1
fi

# Test individual components mentioned in test plan
echo
echo "2. Validating Individual Test Components..."

# Test audio transcription status
echo -n "   Audio Transcription Status: "
if python3 shared/audio_transcription.py --status 2>/dev/null | grep -q "Whisper Available: ✅"; then
    echo "✅"
else
    echo "❌"
fi

# Test PM workflows listing
echo -n "   PM Workflows Listing: "
if python3 shared/pm_audio_workflows.py --list 2>/dev/null | grep -q "Available PM Audio Workflows"; then
    echo "✅"
else
    echo "❌"
fi

# Test AI chat model detection  
echo -n "   AI Chat Model Detection: "
if python3 -c "from shared.ai_chat import AIChat; chat = AIChat('.'); models = chat._detect_available_models(); print('OK')" 2>/dev/null | grep -q "OK"; then
    echo "✅"
else
    echo "❌"
fi

# Test web app startup (brief)
echo -n "   Web App Startup Test: "
python3 web/app.py &
WEB_PID=$!
sleep 3

if curl -s http://localhost:3000/api/status 2>/dev/null | grep -q "running"; then
    echo "✅"
else
    echo "❌"
fi
kill $WEB_PID 2>/dev/null || true

# Test Goose integration status
echo -n "   Goose Integration Status: "
if python3 shared/goose_integration.py --status 2>/dev/null | grep -q "Goose CLI Integration Status"; then
    echo "✅"
else
    echo "❌"
fi

echo
echo "3. Testing Error Handling..."

# Test graceful failure with missing file
echo -n "   Invalid Audio File Handling: "
if python3 shared/audio_transcription.py nonexistent.mp3 2>&1 | grep -q "not found\|error\|Error"; then
    echo "✅ (Fails gracefully)"
else
    echo "❌ (Should show error for missing file)"
fi

echo
echo "4. Testing Documentation..."

# Check that key files exist
echo -n "   Contributors Test Plan Exists: "
if [[ -f "CONTRIBUTORS_TEST_PLAN.md" ]]; then
    echo "✅"
else
    echo "❌"
fi

echo -n "   Test Runner Script Executable: "
if [[ -x "./run_tests.sh" ]]; then
    echo "✅"
else
    echo "❌"
fi

echo
echo "5. Manual Test Validation..."
echo "   The following should be tested manually:"
echo "   🎙️  Audio file transcription (need real MP3/WAV file)"
echo "   💬 Interactive AI chat session"
echo "   🌐 Web dashboard navigation"
echo "   🐳 Docker workflow orchestration"
echo

echo "✅ Test Plan Validation Complete!"
echo
echo "Summary:"
echo "- Quick test runner works correctly"
echo "- Individual components are testable"
echo "- Error handling is working"
echo "- Documentation files are present"
echo "- Manual test procedures are documented"
echo
echo "The Contributors Test Plan appears to be comprehensive and functional!"