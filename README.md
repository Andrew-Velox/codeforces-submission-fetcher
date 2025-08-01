# Codeforces Submission Fetcher

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python tool to fetch and organize your Codeforces submissions with automatic README generation.

![Demo](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- 🚀 Fetches all accepted submissions from your Codeforces account
- 📁 Organizes code files by contest ID
- 📊 Generates a beautiful README table with submission details
- 🔒 Secure API authentication using Codeforces API
- 🏷️ Automatic tagging and categorization
- 📝 Supports multiple programming languages (C++, Python, etc.)

## Prerequisites

- Python 3.8 or higher
- Codeforces API credentials (API Key and Secret)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Andrew-Velox/codeforces-submission-fetcher.git
   cd codeforces-submission-fetcher
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Getting Codeforces API Credentials

1. Go to [Codeforces API Settings](https://codeforces.com/settings/api)
2. Generate your API Key and Secret
3. Keep these credentials secure and never share them publicly

## Usage

### Method 1: Quick Start (Interactive)

Run the script and follow the prompts:

```bash
python CF_FETCH.py
```

You'll be asked to enter:
- Your Codeforces handle (username)
- Your API Key  
- Your API Secret

### Method 2: Using Configuration File (Recommended)

1. Run the setup script to create a configuration file:
   ```bash
   python setup.py
   ```

2. The setup will create a `config.py` file with your credentials

3. Run the main script:
   ```bash
   python CF_FETCH.py
   ```

**Note:** The `config.py` file is automatically ignored by git for security.

The tool will:
1. Fetch all your accepted submissions
2. Save code files organized by contest in the `submissions/` folder
3. Generate a `codeforces_submissions.json` with metadata
4. Create a `README.md` with a formatted table of all submissions

## Project Structure

```
codeforces-fetcher/
├── CF_FETCH.py                  # Main script
├── setup.py                     # Setup script for configuration
├── requirements.txt             # Python dependencies
├── config_template.py           # Configuration template
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore file
├── config.py                   # Your credentials (created by setup.py)
├── submissions/                # Generated folder with code files
│   ├── 1234/                  # Contest ID folders
│   │   ├── A.cpp              # Problem solutions
│   │   └── B.py
│   └── ...
└── codeforces_submissions.json  # Metadata file
```

## Output Example

The generated README will contain a table like this:

| # | Title | Solution | Tags | Submitted |
|:-:|-------|----------|------|-----------|
| 1 | [A - Watermelon](https://codeforces.com/contest/4/problem/A) | [GNU C++17](https://codeforces.com/contest/4/submission/123456789) | `brute force` `math` | Dec/15/2024 14:30 |
| 2 | [B - Way Too Long Words](https://codeforces.com/contest/71/problem/A) | [Python 3](https://codeforces.com/contest/71/submission/123456788) | `strings` | Dec/14/2024 16:22 |

See [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md) for a complete example.

## 📁 Where to Find Your Generated Files

After running the script successfully, you'll find the following files in your current directory:

### Generated Files:
- **`README.md`** - A beautifully formatted table of all your submissions
- **`codeforces_submissions.json`** - Metadata file with detailed information
- **`submissions/`** folder - Contains all your code files organized by contest ID

### 🚀 Upload Your Submissions to GitHub

Once you have your generated `README.md` and `submissions/` folder, you can create a showcase repository:

1. **Create a new repository on GitHub** (e.g., "SolvedProblems" or "MyCodeforcesSolutions")

2. **Upload your files**:
   ```bash
   # Create a new directory for your solutions
   mkdir MyCodeforcesSolutions
   cd MyCodeforcesSolutions
   
   # Copy the generated files
   cp ../README.md .
   cp -r ../submissions .
   cp ../codeforces_submissions.json .
   
   # Initialize git and upload
   git init
   git add .
   git commit -m "My Codeforces solved problems"
   git branch -M main
   git remote add origin https://github.com/yourusername/SolvedProblems.git
   git push -u origin main
   ```

3. **Your repository will now showcase**:
   - ✅ A professional README with all your solved problems
   - 📂 Organized code files by contest
   - 🏷️ Problem tags and submission details
   - 📊 Automatic links to original problems and submissions

**Example repository names**: `SolvedProblems`, `MyCodeforcesSolutions`, `CP-Solutions`, `AlgorithmicSolutions`

## Configuration

You can modify the following variables in the script:
- `SAVE_DIR`: Directory to save submission files (default: "submissions")
- `JSON_FILE`: Metadata file name (default: "codeforces_submissions.json")
- `README_FILE`: Output README file name (default: "README.md")

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with Codeforces. Please respect Codeforces' terms of service and API rate limits.

## Support

If you encounter any issues or have suggestions, please open an issue on GitHub.
