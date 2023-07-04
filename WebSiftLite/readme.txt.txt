-------------------------------------------------------------------------------
                        WebSiftLite - Webpage Scraper
-------------------------------------------------------------------------------

WebSiftLite is a simple and robust webpage scraper written in Python. It utilizes the built-in libraries in Python to make HTTP requests, parse HTML and handle errors efficiently.

FEATURES:

1. Scrapes and prints headers, links, and text content from a webpage.
2. Performs error handling in case of timeouts, SSL errors, etc.
3. Uses an HTMLParser to parse the HTML content from the webpage.
4. Allows multiple attempts to fetch the webpage content.

USAGE:

To use WebSiftLite, run the python script in your console. You will be presented with a menu with two options:

1. Scrape a website
2. Exit

Choose option 1 to input a website URL that you wish to scrape. The scraper will fetch the content, parse the HTML, and print out the headers, links, and text content.

Choose option 2 to exit the program.

Note: Make sure the URL you enter starts with 'http' or 'https'. Incorrect or invalid URLs will not be accepted.

DEPENDENCIES:

Python 3.6 or higher.
