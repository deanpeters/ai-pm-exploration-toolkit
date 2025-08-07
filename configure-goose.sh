#!/bin/bash

# Script to configure Goose CLI for AI PM Toolkit
# This automates the interactive configuration process

export PATH="/Users/deanpeters/.local/bin:$PATH"

# Remove any existing configuration
rm -f /Users/deanpeters/.config/goose/config.yaml

echo "Configuring Goose CLI for AI PM Toolkit..."
echo "This will set up Ollama provider with qwen2.5 model"

# Create expect script to handle interactive configuration
expect << 'EOF'
spawn goose configure
expect "Let's get you set up with a provider."
send "\r"
expect "Configure Providers"
send "1\r"
expect "Select a provider:"
send "2\r"
expect "Ollama Host:"
send "http://localhost:11434\r"
expect "Model:"
send "qwen2.5\r"
expect eof
EOF

echo "Goose CLI configuration completed!"

# Test the configuration
echo "Testing Goose CLI..."
goose info