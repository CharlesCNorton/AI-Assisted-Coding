# SimpleScraper - This program scrapes a website and displays it in clean text.
# This code was created with Google Bard and GPT-4 on 2023-06-08 08:29:31 PST.

"""
Welcome to SimpleScraper!
"""

import requests
from bs4 import BeautifulSoup

def render_website(url, line_numbers=False, line_length=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to fetch the website: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
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

def main():
    while True:
        url = input("Enter the URL of the website (including http or https) or 'q' to quit: ")
        if url.lower() == 'q':
            break
        line_numbers = input("Show line numbers? (y/n): ").lower() == 'y'
        line_length = input("Maximum line length (leave blank for no limit): ")
        line_length = int(line_length) if line_length else None
        render_website(url, line_numbers=line_numbers, line_length=line_length)

if __name__ == "__main__":
    main()
