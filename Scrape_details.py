import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, 'html.parser')
for quote_block in soup.find_all('div', class_='quote'):
    quote = quote_block.find('span', class_='text').text.strip()
    author = quote_block.find('small', class_='author').text.strip()
    print(f"{quote} ----- {author}")
# print(f"Number of quote blocks on the page: {len(quotes)}")