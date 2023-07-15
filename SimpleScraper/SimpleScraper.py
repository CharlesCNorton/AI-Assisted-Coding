"""
Welcome to SimpleScraper!
"""

import requests
from bs4 import BeautifulSoup

def get_website_content(url):
    """Fetch the website content"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.content
    except requests.exceptions.Timeout:
        print("The request timed out. Please check your network connection or try again later.")
    except requests.exceptions.TooManyRedirects:
        print("The request exceeded the configured number of maximum redirections.")
    except requests.exceptions.SSLError:
        print("A SSL error occurred.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to fetch the website: {e}")
    return None

def render_website(content, line_numbers=False, line_length=None):
    """Parse and print the website content"""
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.strip()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line:
            if line_numbers:
                print(f"{i+1: >3}: ", end="")
            if line_length:
                print(line[:line_length].rstrip())
            else:
                print(line.rstrip())

def get_url():
    """Prompt user for URL and validate it"""
    while True:
        url = input("Enter the URL of the website (including http or https) or 'q' to quit: ")
        if url.lower() == 'q':
            return None
        elif url.startswith(('http://', 'https://')):
            return url
        else:
            print("Invalid URL. Please try again.")

def get_line_numbers():
    """Prompt user for line numbers and validate input"""
    while True:
        choice = input("Show line numbers? (y/n): ").lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def get_line_length():
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
        url = get_url()
        if url is None:
            break
        line_numbers = get_line_numbers()
        line_length = get_line_length()
        content = get_website_content(url)
        if content is not None:
            render_website(content, line_numbers=line_numbers, line_length=line_length)

if __name__ == "__main__":
    main()