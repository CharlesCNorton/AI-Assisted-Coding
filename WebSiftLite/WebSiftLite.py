import http.client
import ssl
from html.parser import HTMLParser
from urllib.parse import urlparse
import urllib

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
        if self.current_tag is not None and self.current_tag not in ['script', 'style']:
            if self.current_header is not None:
                self.current_header["data"] += data.strip()
            self.text.append({"tag": self.current_tag, "data": data.strip()})

    def error(self, message):
        print("\033[0;31;40mHTML Parser Error:\033[0m", message)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_website_content(site, max_retries=3):
    if not is_valid_url(site):
        print("Invalid URL, please enter a URL starting with http or https.")
        return None

    headers = {"User-Agent": "Mozilla/5.0"}
    parsed_url = urlparse(site)

    for i in range(max_retries):
        try:
            if parsed_url.scheme == 'https':
                conn = http.client.HTTPSConnection(parsed_url.netloc, context=ssl._create_unverified_context())
            else:
                conn = http.client.HTTPConnection(parsed_url.netloc)

            conn.request("GET", parsed_url.path, headers=headers)
            response = conn.getresponse()

            if response.status in [200, 301, 302]:
                return response.read().decode()
            else:
                print("Failed to fetch the webpage, status:", response.status)
                return None
        except (http.client.HTTPException, urllib.error.URLError) as e:
            print(f"Attempt {i+1} of {max_retries} failed: {str(e)}")
        finally:
            conn.close()

    print(f"Failed to fetch the webpage after {max_retries} attempts.")
    return None

def main():
    while True:
        print("1. Scrape a website")
        print("2. Exit")
        while True:
            choice = input("Enter your choice: ")
            if choice in ["1", "2"]:
                break
            print("Invalid choice, please try again.")

        if choice == "1":
            site = input("Enter a website to scrape (e.g. https://www.example.com): ")
            content = get_website_content(site)
            if content:
                parser = MyHTMLParser()
                try:
                    parser.feed(content)
                except Exception as e:
                    print("\033[0;31;40mError parsing the content:\033[0m", e)
                    continue

                print("\033[1;32;40mHeaders on the page:\033[0m")
                for header in parser.headers:
                    print(f"\033[1;31;40m{header['tag']}:\033[0m {header['data']}")

                print("\n\033[1;32;40mLinks on the page:\033[0m")
                for link in parser.links:
                    print(link)

                print("\n\033[1;32;40mText on the page:\033[0m")
                last_tag = None
                for text in parser.text:
                    if text['data']:  # Only print if there is some data
                        if text['tag'] != last_tag:
                            print(f"\n\033[1;34;40m{text['tag']}:\033[0m")
                            last_tag = text['tag']
                        print(text['data'])
        elif choice == "2":
            break

if __name__ == "__main__":
    main()
