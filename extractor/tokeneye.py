#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
import sys

def scrape(chain, url, output_dir):

    token_data = []  
    now = datetime.now()

    for page in range(1, 10):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url + str(page), headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            token_table = soup.find('div', class_='table-responsive')
            rows = token_table.find_all('tr')

            for row in rows:
                columns = row.find_all('td')

                if len(columns) >= 2:
                    index = columns[0].text.strip()
                    token_name = columns[1].text.strip()

                    link = columns[1].find('a')
                    href = link.get('href')
                    holders = columns[7].text.strip()

                    # Aggiungi i dati del token alla lista
                    token_data.append({
                        'chain': chain,
                        'ts': now.isoformat(),
                        'name': re.sub('\\\n', ' ', token_name),
                        'hash': re.sub('/token/', '', href),
                        'holders': re.sub('\\\n', '', re.sub(r'(-)?\d+(\.\d+)?%', '', holders))
                    })
        else:
            print(f"Error retrieving HTTP data. Status code: {response.status_code}")

    json_output = json.dumps(token_data, indent=2)
    #print(json_output)

    file_name = f"{chain}_{int(time.time())}.json"

    save_path = output_dir + "/" + file_name
    with open(save_path, 'w') as file:
        file.write(json_output)
    
    print(f"Done " + file_name)

output_dir = sys.argv[1]

scrape("ethereum", "https://etherscan.io/tokens?&sort=holders&order=asc&p=", output_dir)
scrape("bsc", "https://bscscan.com/tokens?sort=holders&order=asc&p=", output_dir)
