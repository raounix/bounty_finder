import requests
from pathlib import Path
import schedule
import time


domains_raw = requests.get('https://github.com/arkadiyt/bounty-targets-data/blob/main/data/domains.txt')
wildCards_raw = requests.get('https://github.com/arkadiyt/bounty-targets-data/blob/main/data/wildcards.txt')

domains = domains_raw.json()["payload"]["blob"]['rawLines']
wildCards = wildCards_raw.json()["payload"]["blob"]['rawLines']


def check_file_exist(file_name,urls):
    file_exist_check = Path(file_name)
    if not file_exist_check.is_file():
        bulk_file = open(file_name, 'w')
        for url in urls:
            bulk_file.writelines(url+"\n")
        bulk_file.close()

def check_difference_urls(file_path, url_array):
    new_url_lists = []
    with open(file_path, 'r+') as file:
        old_data_lines = file.readlines()
        for new_url in url_array:
            if (new_url+"\n") not in old_data_lines:
                file.writelines(new_url+"\n")
                new_url_lists.append(new_url)
    return new_url_lists
if __name__ == "__main__":
    check_file_exist("./db/domains.txt",domains)
    check_file_exist("./db/wildcards.txt",wildCards)

    while True:
        print("run")
        new_domains = check_difference_urls("./db/domains.txt",domains)
        new_wildCards = check_difference_urls("./db/wildcards.txt",wildCards)
        time.sleep(5)