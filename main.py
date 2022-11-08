import csv
import re
import requests
from bs4 import BeautifulSoup


def go():
    start_year =1956
    most_recent_year = 2022
    year_counter = start_year

    header = ['Contest Year', 'R/O', 'Country', 'Artist', 'Song', 'Language', 'Points', 'Place']
    with open('euro_pop.csv', 'a', newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(header)

    while year_counter <= most_recent_year:
        if year_counter != 2020:
            print("Scraping year: " + str(year_counter))
            scrape(year_counter)
        year_counter += 1


def scrape(year):
    url = "https://en.wikipedia.org/wiki/Eurovision_Song_Contest_" + str(year)
    print("URL: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    tables = soup.findAll('table')
    results_tables = []

    for table in tables:
        ths = table.find_all('th')
        headings = [th.text.strip() for th in ths]
        if headings:
            if 'R/O' in headings[0]:
                print('Found results table!')
                results_tables.append(table)

    table = results_tables[-1]
    rows = []
    data_rows = table.find_all('tr')
    headers = [header.text.strip() for header in table.find_all(scope="col")]
    headers.insert(0, 'Contest Year')

    # Get running order data first
    running_order_rows = []
    for row in data_rows:
        running_order = row.find_all(scope="row")
        beautified_value = [ele.text.strip() for ele in running_order]
        if len(beautified_value) == 0:
            continue
        running_order_rows.append(beautified_value)

    # Get everything else
    for row in data_rows:
        value = row.find_all('td')
        beautified_value = [ele.text.strip() for ele in value]
        # Remove data arrays that are empty
        if len(beautified_value) == 0:
            continue

        # Remove any citations that have made it through
        for item in beautified_value:
            current_index = beautified_value.index(item)
            beautified_value[current_index] = re.sub(r'\[.*\]', '', item)

        rows.append(beautified_value)

    for entry in rows:
        position = rows.index(entry)
        entry.insert(0, str(year))
        entry.insert(1, running_order_rows[position][0])

    with open('euro_pop.csv', 'a', newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerows(rows)

if __name__ == '__main__':
    go()
