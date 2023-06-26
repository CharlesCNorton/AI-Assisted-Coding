import http.client
import ssl
from html.parser import HTMLParser
from urllib.parse import urlparse

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.current_header = None
        self.headers = []
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_header = {"tag": tag, "data": ""}
        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.current_header is not None:
            self.headers.append(self.current_header)
            self.current_header = None
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag is not None:
            if self.current_header is not None:
                self.current_header["data"] += data.strip()
            self.text.append({"tag": self.current_tag, "data": data.strip()})

def get_website_content(site):
    parsed_url = urlparse(site)
    if parsed_url.scheme not in ['http', 'https']:
        print("Invalid URL, please enter a URL starting with http or https.")
        return None

    try:
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(parsed_url.netloc, context=ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc)

        conn.request("GET", parsed_url.path)
        response = conn.getresponse()

        if response.status == 200:
            return response.read().decode()
        else:
            print("Failed to fetch the webpage, status:", response.status)
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    while True:
        print("1. Scrape a website")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            site = input("Enter a website to scrape (e.g. https://www.example.com): ")
            content = get_website_content(site)
            if content:
                parser = MyHTMLParser()
                parser.feed(content)
                print("Headers on the page:")
                for header in parser.headers:
                    print(f"{header['tag']}: {header['data']}")
                print("Links on the page:")
                for link in parser.links:
                    print(link)
                print("Text on the page:")
                for text in parser.text:
                    if text['data']: # Only print if there is some data
                        print(f"{text['tag']}: {text['data']}")
        elif choice == "2":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
