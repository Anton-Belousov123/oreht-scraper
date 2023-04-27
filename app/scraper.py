import datetime
import time
import lxml
import requests
import bs4
import dataclasses

@dataclasses.dataclass
class Item:
    name: str
    url: str
    photo: str
    article: str
    price: float


class Scraper:
    def scrape_item(self, item_code: int):
        url = f"https://www.oreht.ru/modules.php?name=orehtPriceLS&op=ShowInfo&code={item_code}"
        response = requests.get(url=url)
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        name = soup.find("div", {"class": "mg-h1text"}).text
        img = soup.find("div", {"class": "mg-glimage"}).find("img").get("src")
        price = soup.find("div", {"class": "mg-price"})
        name = name.strip()
        img = "https://www.oreht.ru/" + img.strip()
        price = float(
            price.find("span", "mg-price-n").text.strip() + "." + price.find_all("span", "mg-price-n")[1].text.strip())
        return Item(
            name=name,
            url=url,
            photo=img,
            article=item_code,
            price=price
        )

