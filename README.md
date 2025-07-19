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

## TODO: Improvements
* rename folder to expanded_pom
* rename old to legacy or something else to clearly mark they are inferior and the expanded is my main one
* see below and rename pom_demo and associated references to basic_pom_demo


## Projects

| Project Folder        | Description                               |
|-----------------------|-------------------------------------------|
| `procedural_tests/`   | First experiments with Selenium in Python |
| `basic_pom_demo/`           | Basic Page Object Model practice          |
| `expanded_pom_demo/`  | ✅ Main showcase with advanced POM style  |

"This repository contains three progressive tiers of automation test examples, starting with an introductory POM demo and culminating in a polished, multi-page framework (expand_pom_demo) showcasing professional test design."

Put in multiple READMEs

/your-repo-root/
│
├── README.md                  ← 🧭 Top-level: overview of your entire repo
│
├── procedural_tests/
│   └── README.md              ← 📝 Describes your early procedural tests
│
├── pom_demo/
│   └── README.md              ← 📝 Describes your first POM-based tests
│
└── expanded_pom_demo/
    └── README.md              ← ✅ Highlight your main showcase project