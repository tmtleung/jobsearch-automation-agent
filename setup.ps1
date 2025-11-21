Write-Host "Setting up linkedin-jobsearch-ai-agent..."

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Copy config template if missing
if (-Not (Test-Path "config\config.json")) {
    Copy-Item "config\config.example.json" "config\config.json"
    Write-Host "Created config\config.json from template."
} else {
    Write-Host "config\config.json already exists. Skipping."
}

Write-Host "`nSetup complete!"
Write-Host "Next steps:"
Write-Host "  1. Edit config\config.json to customize your job search."
Write-Host "  2. Run the agent with: python run_agent.py"
Write-Host ""
