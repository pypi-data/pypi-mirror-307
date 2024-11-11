#!/usr/bin/env python3
import os
import json
import uuid
import platform
import subprocess
import sys
from pathlib import Path

def get_config_dir():
    app_name = "kusho"
    if platform.system() == "Windows":
        config_dir = os.path.join(os.getenv('APPDATA'), app_name)
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config", app_name)
    return config_dir

def ensure_uuid():
    config_dir = get_config_dir()
    uuid_file = os.path.join(config_dir, "saved_uuid.txt")
    os.makedirs(config_dir, exist_ok=True)
    
    if os.path.exists(uuid_file):
        with open(uuid_file, 'r') as f:
            saved_uuid = f.read().strip()
            print(f"Saved UUID: {saved_uuid}")
            return saved_uuid
    else:
        new_uuid = str(uuid.uuid4())
        with open(uuid_file, 'w') as f:
            f.write(new_uuid)
        print(f"New UUID generated and saved: {new_uuid}")
        return new_uuid

def get_user_input(prompt, default=""):
    user_input = input(f"{prompt}: ").strip()
    return user_input if user_input else default

def extract_value(json_str, key):
    try:
        data = json.loads(json_str)
        return data.get(key, "")
    except json.JSONDecodeError:
        return ""

def execute_test_case(test_case):
    method = extract_value(test_case, "method")
    url = extract_value(test_case, "url")
    headers = extract_value(test_case, "headers")
    path_params = extract_value(test_case, "path_params")
    query_params = extract_value(test_case, "query_params")
    json_body = extract_value(test_case, "json_body")

    # Process URL with path parameters
    if path_params and path_params != "{}":
        for key, value in json.loads(path_params).items():
            url = url.replace(f"{{{key}}}", str(value))

    # Add query parameters
    if query_params and query_params != "{}":
        query_parts = []
        for key, value in json.loads(query_params).items():
            query_parts.append(f"{key}={value}")
        if query_parts:
            url = f"{url}?{'&'.join(query_parts)}"

    # Prepare curl command
    curl_cmd = ["curl", "-X", method, url]
    
    # Add headers
    if headers and headers != "{}":
        for key, value in json.loads(headers).items():
            curl_cmd.extend(["-H", f"{key}: {value}"])
    
    curl_cmd.extend(["-H", "Content-Type: application/json"])
    
    # Add body if present
    if json_body and json_body != "{}":
        curl_cmd.extend(["-d", json_body])

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")

def main():
    config_dir = get_config_dir()
    test_file = os.path.join(config_dir, "tests.json")
    Path(test_file).touch()

    saved_uuid = ensure_uuid()

    # Collect API details
    test_suite_name = get_user_input("Enter the test suite name (optional)")
    method = get_user_input("Enter the HTTP method (e.g., GET, POST)", "GET")
    url = get_user_input("Enter the API URL", "https://example.com")
    api_desc = get_user_input("Enter a description for this API (optional)")
    headers = get_user_input('Enter headers as a JSON string (e.g., {"Content-Type":"application/json"})', "{}")
    path_params = get_user_input('Enter path parameters as a JSON string (e.g., {"id":"123"})', "{}")
    query_params = get_user_input('Enter query parameters as a JSON string (e.g., {"key":"value"})', "{}")
    json_body = get_user_input('Enter JSON body (optional, e.g., {"data":"value"})', "{}")

    # Prepare API info
    api_info = {
        "method": method,
        "url": url,
        "api_desc": api_desc,
        "headers": json.loads(headers),
        "path_params": json.loads(path_params),
        "query_params": json.loads(query_params),
        "json_body": json.loads(json_body)
    }

    payload = {
        "machine_id": saved_uuid,
        "api_info": api_info,
        "test_suite_name": test_suite_name
    }

    # Make request to generate tests
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "https://be.kusho.ai/vscode/generate/streaming",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload)],
            capture_output=True,
            text=True
        )
        
        test_cases = []
        for line in result.stdout.split('\n'):
            if line.startswith('data:'):
                test_cases.append(line[5:])  # Remove 'data:' prefix
                with open(test_file, 'a') as f:
                    f.write(line[5:] + '\n')

        # Menu loop
        while True:
            print("\nSelect an option:")
            print("1. List all test cases")
            print("2. Execute all test cases")
            print("3. Run a specific test case")
            print("4. Exit")
            
            choice = input("Enter your choice (1, 2, 3 or 4): ")
            
            if choice == '1':
                for i, test_case in enumerate(test_cases, 1):
                    print(f"\nTest Case {i}:")
                    print(test_case)
                    print("-" * 20)
            
            elif choice == '2':
                for test_case in test_cases:
                    execute_test_case(test_case)
            
            elif choice == '3':
                try:
                    test_index = int(input(f"Enter the test case number (1-{len(test_cases)}): "))
                    if 1 <= test_index <= len(test_cases):
                        execute_test_case(test_cases[test_index - 1])
                    else:
                        print("Invalid test case number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == '4':
                print("Exiting.")
                break
            
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")

    except subprocess.CalledProcessError as e:
        print(f"Error making request: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()