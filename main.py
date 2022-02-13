from bs4 import BeautifulSoup
import requests
import lxml
from src.constants import START_PAGE, PAGE_PATTERN
import csv

URLS = [START_PAGE]
COLUMN = ["recipient", "amount"]
DATA = [COLUMN]

pageNum = range(2, 19)
for page_number in pageNum:
    URLS.append(PAGE_PATTERN.format(page_number))

for url in URLS:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find("tbody")
    contents = tbody.contents
    recipient, amount = None, None
    for index, content in enumerate(contents):
        text_content = content.text
        if text_content != '\n':
            now_text_content = text_content
            content_list = now_text_content.split('\n')
            for elem in content_list:
                if elem not in ("'", '"', "\n") and elem:
                    if elem.startswith("Заказчик:"):
                        recipient = {"value": elem.split(':')[1], "content": index}
                    if elem.replace(' ', '').replace(' ', '').isdigit():
                        amount = {"value": elem.replace(' ', '').replace(' ', ''), "content": index}
                    if recipient and amount and amount["content"] == recipient["content"] and [recipient["value"], amount["value"]] not in DATA:
                        DATA.append([recipient["value"].replace('""', '"').replace("''", "'"), amount["value"]])


with open("recipient_amount.csv", mode='a', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerows(DATA)
