#!/bin/bash

echo "Setting up linkedin-jobsearch-ai-agent..."

# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy config template
if [ ! -f config/config.json ]; then
    cp config/config.example.json config/config.json
    echo "Created config/config.json from template."
else
    echo "config/config.json already exists, skipping copy."
fi

echo "Setup complete!"
echo "Next steps:"
echo "1. Edit config/config.json to customize your search."
echo "2. Run the agent with: python run_agent.py"

