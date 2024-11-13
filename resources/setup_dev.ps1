# Powershell script to setup the entire project as a virtual environment for you
# setup_dev.ps1

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\activate

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".\.env")) {
    Write-Host "Creating .env file from template..."
    copy .env.example .env
    Write-Host "Please update the .env file with your configuration values"
}

# Install pre-commit hooks if git is initialized
if (Test-Path ".git") {
    Write-Host "Installing pre-commit hooks..."
    pip install pre-commit
    pre-commit install
}

Write-Host "Setup complete! Your development environment is ready."
Write-Host "Don't forget to:"
Write-Host "1. Update your .env file with your actual configuration"
Write-Host "2. Run 'deactivate' when you're done to exit the virtual environment"