#!/usr/bin/env python3
"""
Codeforces Submission Fetcher

A tool to fetch and organize your Codeforces submissions with automatic README generation.
Fetches all accepted submissions from your Codeforces account and organizes them into
a structured format with metadata and documentation.

Author: Your Name
License: MIT
"""

import os
import json
import requests
import hashlib
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

# ========== CONFIG START ==========
SAVE_DIR = "submissions"
JSON_FILE = "codeforces_submissions.json"
README_FILE = "README.md"
API_BASE_URL = "https://codeforces.com/api"
# ========== CONFIG END ==========

def get_api_signature(method: str, params: Dict[str, str], api_key: str, api_secret: str) -> str:
    """
    Generate API signature for Codeforces API authentication.
    
    Args:
        method: API method name
        params: API parameters
        api_key: Codeforces API key
        api_secret: Codeforces API secret
        
    Returns:
        Generated API signature
    """
    rand = "123456"
    params["apiKey"] = api_key
    params["time"] = str(int(time.time()))
    sorted_items = sorted(params.items())
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_items])
    string_to_hash = f"{rand}/{method}?{query_string}#{api_secret}"
    hash_code = hashlib.sha512(string_to_hash.encode()).hexdigest()
    return rand + hash_code

def fetch_submissions(handle: str, api_key: str, api_secret: str) -> List[Dict[str, Any]]:
    """
    Fetch submissions from Codeforces API.
    
    Args:
        handle: Codeforces username
        api_key: Codeforces API key
        api_secret: Codeforces API secret
        
    Returns:
        List of submission data
        
    Raises:
        Exception: If API request fails
    """
    method = "user.status"
    url = f"{API_BASE_URL}/{method}"
    params = {
        "handle": handle
    }
    api_sig = get_api_signature(method, params.copy(), api_key, api_secret)
    params["apiSig"] = api_sig

    print(f"Fetching submissions for user: {handle}...")
    try:
        resp = requests.get(url, params=params, timeout=30).json()
        if resp["status"] != "OK":
            raise Exception(f"API Error: {resp.get('comment', 'Unknown error')}")
        return resp["result"]
    except requests.RequestException as e:
        raise Exception(f"Network error: {e}")
    except json.JSONDecodeError:
        raise Exception("Invalid response from Codeforces API")

def save_code_and_metadata(submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Save submission code files and generate metadata.
    
    Args:
        submissions: List of submission data from API
        
    Returns:
        Dictionary containing metadata for all submissions
    """
    accepted = {}
    for sub in submissions:
        if sub.get("verdict") != "OK":
            continue

        key = f'{sub["contestId"]}-{sub["problem"]["index"]}'
        if key in accepted and sub["creationTimeSeconds"] < accepted[key]["creationTimeSeconds"]:
            continue
        accepted[key] = sub

    metadata = {}
    count = len(accepted)
    print(f"Processing {count} latest accepted submissions...")

    for i, sub in enumerate(sorted(accepted.values(), key=lambda x: -x["creationTimeSeconds"])):
        problem = sub["problem"]
        contest_id = sub["contestId"]
        index = problem["index"]
        name = problem["name"]
        url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
        sub_id = f"CF{sub['id']}"
        sub_url = f"https://codeforces.com/contest/{contest_id}/submission/{sub['id']}"
        lang = sub["programmingLanguage"]
        tags = problem.get("tags", [])
        dt = datetime.fromtimestamp(sub["creationTimeSeconds"])
        ts = dt.strftime("%b/%d/%Y %H:%M")

        folder = os.path.join(SAVE_DIR, str(contest_id))
        os.makedirs(folder, exist_ok=True)
        
        # Determine file extension based on programming language
        ext = get_file_extension(lang)
        filepath = os.path.join(folder, f"{index}{ext}")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(sub.get("program", "// Code not available"))
        except Exception as e:
            print(f"Warning: Could not save file {filepath}: {e}")

        metadata[sub_id] = {
            "contest_id": contest_id,
            "language": lang,
            "path": filepath.replace("/", "\\"),
            "problem_index": index,
            "problem_name": name,
            "problem_url": url,
            "submission_id": sub_id,
            "submission_url": sub_url,
            "tags": tags,
            "timestamp": ts
        }

    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to {JSON_FILE}")
    except Exception as e:
        print(f"Warning: Could not save metadata file: {e}")
        
    return metadata

def get_file_extension(language: str) -> str:
    """
    Get appropriate file extension based on programming language.
    
    Args:
        language: Programming language name
        
    Returns:
        File extension including the dot
    """
    language_lower = language.lower()
    if "c++" in language_lower or "cpp" in language_lower:
        return ".cpp"
    elif "python" in language_lower:
        return ".py"
    elif "java" in language_lower:
        return ".java"
    elif "javascript" in language_lower:
        return ".js"
    elif "c#" in language_lower or "csharp" in language_lower:
        return ".cs"
    elif "go" in language_lower:
        return ".go"
    elif "rust" in language_lower:
        return ".rs"
    else:
        return ".txt"

def generate_readme(metadata: Dict[str, Any]) -> None:
    """
    Generate README.md file with formatted submission table.
    
    Args:
        metadata: Dictionary containing submission metadata
    """
    if not metadata:
        print("No submissions found to generate README.")
        return
        
    rows = []
    sorted_meta = list(metadata.items())
    sorted_meta.sort(key=lambda x: -int(x[0].replace("CF", "")))

    for i, (sub_id, data) in enumerate(sorted_meta, 1):
        tags_str = ' '.join(f'`{tag}`' for tag in data['tags']) if data['tags'] else 'No tags'
        row = f"| {i} | [{data['problem_index']} - {data['problem_name']}]({data['problem_url']}) | [{data['language']}]({data['submission_url']}) | {tags_str} | {data['timestamp']} |"
        rows.append(row)

    table = [
        "| # | Title | Solution | Tags | Submitted |",
        "|:-:|-------|----------|------|-----------|",
        *rows
    ]

    try:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("# Codeforces Submissions\n\n")
            f.write(f"Total accepted submissions: **{len(metadata)}**\n\n")
            f.write("---\n\n")
            f.write("\n".join(table))
            f.write("\n\n---\n\n")
            f.write("*Generated automatically by [Codeforces Submission Fetcher](https://github.com/Andrew-Velox/codeforces-submission-fetcher)*\n")
        print(f"README.md generated successfully with {len(metadata)} submissions.")
    except Exception as e:
        print(f"Error generating README: {e}")

def get_user_input() -> tuple:
    """
    Get user credentials through command line input or config file.
    
    Returns:
        Tuple containing (handle, api_key, api_secret)
    """
    # Try to load from config file first
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    if os.path.exists(config_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)
            if hasattr(config, 'HANDLE') and hasattr(config, 'API_KEY') and hasattr(config, 'API_SECRET'):
                if config.HANDLE and config.API_KEY and config.API_SECRET:
                    print("✅ Using credentials from config.py")
                    return config.HANDLE, config.API_KEY, config.API_SECRET
        except Exception as e:
            print(f"Warning: Could not load config.py: {e}")
    # Fall back to interactive input
    
    # Fall back to interactive input
    print("=== Codeforces Submission Fetcher ===")
    print("Please enter your Codeforces API credentials:")
    print("(You can get them from: https://codeforces.com/settings/api)")
    print("(Or create a config.py file - see config_template.py for reference)\n")
    
    handle = input("Enter your Codeforces handle: ").strip()
    if not handle:
        raise ValueError("Handle cannot be empty")
        
    api_key = input("Enter your API key: ").strip()
    if not api_key:
        raise ValueError("API key cannot be empty")
        
    api_secret = input("Enter your API secret: ").strip()
    if not api_secret:
        raise ValueError("API secret cannot be empty")
    
    return handle, api_key, api_secret

def main():
    """Main function to orchestrate the submission fetching process."""
    try:
        # Get user credentials
        handle, api_key, api_secret = get_user_input()
        
        # Fetch submissions
        submissions = fetch_submissions(handle, api_key, api_secret)
        
        if not submissions:
            print("No submissions found for this user.")
            return
            
        # Process and save submissions
        metadata = save_code_and_metadata(submissions)
        
        # Generate README
        generate_readme(metadata)
        
        print(f"\n✅ Successfully processed {len(metadata)} accepted submissions!")
        print(f"📁 Code files saved in: {SAVE_DIR}/")
        print(f"📊 Metadata saved in: {JSON_FILE}")
        print(f"📝 README generated: {README_FILE}")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
