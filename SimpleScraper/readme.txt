## SimpleScraper

SimpleScraper is a Python program that retrieves and displays the content of a website in clean text format. This script fetches the raw HTML content from the specified website and parses it using BeautifulSoup to remove HTML tags and display the text content.

## Features

1. Fetch and display content from any website
2. Option to print line numbers alongside the text content
3. Option to limit the length of lines displayed
4. Enhanced error handling to manage network issues and invalid URLs
5. Improved user prompts for better user experience

## Dependencies

The program requires the following Python libraries:

- requests
- BeautifulSoup

## Usage

Run the script from the terminal using Python:

python simple_scraper.py

The script will prompt you for a URL. Enter a URL starting with 'http://' or 'https://'. To quit, simply type 'q' and press enter.

Next, you'll be asked if you want to display line numbers. Enter 'y' for yes or 'n' for no.

Finally, you'll be asked for the maximum line length. Enter a positive integer to limit the line length or leave it blank for no limit.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you'd like to add.