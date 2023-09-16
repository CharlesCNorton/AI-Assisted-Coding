"""
Welcome to SimpleScraper!
"""

import requests
from bs4 import BeautifulSoup

ERROR_MESSAGES = {
    "Timeout": "The request timed out. Please check your network connection or try again later.",
    "TooManyRedirects": "The request exceeded the configured number of maximum redirections.",
    "SSLError": "A SSL error occurred.",
    "RequestException": "An error occurred while trying to fetch the website."
}

def fetch_website_content(url):
    """Fetch the website content"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        error_type = type(e).__name__
        print(ERROR_MESSAGES.get(error_type, f"An error occurred: {e}"))
        return None

def render_website(content, line_numbers=False, line_length=None):
    """Parse and print the website content"""
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text().strip()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line:
            prefix = f"{i+1: >3}: " if line_numbers else ""
            line_content = line[:line_length].rstrip() if line_length else line.rstrip()
            print(f"{prefix}{line_content}")

def prompt_url():
    """Prompt user for URL and validate it"""
    while True:
        url = input("Enter the URL of the website (including http or https) or 'q' to quit: ")
        if url.lower() == 'q':
            return None
        elif url.startswith(('http://', 'https://')):
            return url
        else:
            print("Invalid URL. Please try again.")

def prompt_for_boolean(message, true_option='y', false_option='n'):
    """Prompt user for a boolean choice and validate input"""
    while True:
        choice = input(message).lower()
        if choice == true_option:
            return True
        elif choice == false_option:
            return False
        else:
            print(f"Invalid input. Please enter '{true_option}' or '{false_option}'.")

def prompt_line_length():
    """Prompt user for line length and validate it"""
    while True:
        line_length = input("Maximum line length (leave blank for no limit): ")
        if not line_length:
            return None
        elif line_length.isdigit() and int(line_length) > 0:
            return int(line_length)
        else:
            print("Invalid input. Please enter a positive number.")

def main():
    while True:
        url = prompt_url()
        if url is None:
            break
        line_numbers = prompt_for_boolean("Show line numbers? (y/n): ")
        line_length = prompt_line_length()
        content = fetch_website_content(url)
        if content is not None:
            render_website(content, line_numbers=line_numbers, line_length=line_length)

if __name__ == "__main__":
    main()