# Selenium Test Suite
This project contains automated UI tests using **Selenium + Pytest**, built for skill development and showcasing QA engineering practices.

## Features

- Uses **Pytest fixtures**
- Modular **Page Object-like helpers** in `utils/`
- Run tests individually or as a suite
- Configured for **VS Code debugging** via `launch.json`

## Setup

```bash
git clone https://github.com/bcaloz/selenium-tests.git
cd selenium-tests
python -m venv venv                 # creates the virtual environment `venv` inside the venv/ folder
.\venv\Scripts\Activate.ps1         # use this to activate it in PowerShell on Windows
venv\Scripts\activate.bat           # use this to activate it in CMD on Windows
source venv/bin/activate            # use this to activate in Git Bash/WSL/Linux/Mac
pip install -r requirements.txt     # to recreate environment
pytest tests/
