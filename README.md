# Selenium Test Suite
This project contains automated UI tests using **Selenium + Pytest**, built for skill development and showcasing QA engineering practices.

## Features

- Uses **Pytest** test runner with **fixture-based** WebDriver setup
- Two test styles:
    - **Legacy**: procedural tests using reusable helpers in `utils/`
    - **Modern**: Page Object Model (POM) tests in `pom_demo/pages/`
- Run tests individually or as a suite
- Configured for **debugging in VS Code** via `launch.json`
- Tested with ChromeDriver locally
- Supports **headless mode** via Chrome options (toggle in `conftest.py`)

## Setup

```bash
git clone https://github.com/bcaloz/selenium-tests.git
cd selenium-tests
python -m venv venv                 # Set up virtual environment

# Activate (pick one)
.\venv\Scripts\Activate.ps1         # PowerShell (Windows)
venv\Scripts\activate.bat           # CMD (Windows)
source venv/bin/activate            # Git Bash/WSL/Linux/Mac

# Install dependencies
pip install -r requirements.txt     
```

## Test execution
```bash
# Run procedural tests
pytest tests/ -v

# Run POM-based tests
pytest pom_demo/tests/ -v
```