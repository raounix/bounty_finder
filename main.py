import requests
from pathlib import Path
import time
import requests
import json


############################################################
def get_new_domains_update():
    domains_raw = requests.get('https://github.com/arkadiyt/bounty-targets-data/blob/main/data/domains.txt')
    wildCards_raw = requests.get('https://github.com/arkadiyt/bounty-targets-data/blob/main/data/wildcards.txt')

    domains = domains_raw.json()["payload"]["blob"]['rawLines']
    wildCards = wildCards_raw.json()["payload"]["blob"]['rawLines']
    print("checking file complete")
    return domains,wildCards
############################################################


############################################################
def read_config_file():
    config_file = open('./config/telegram.json', 'r')
    data = json.load(config_file)
    return data
############################################################

############################################################
def check_file_exist(file_name,urls):
    file_exist_check = Path(file_name)
    if not file_exist_check.is_file():
        bulk_file = open(file_name, 'w')
        for url in urls:
            bulk_file.writelines(url+"\n")
        bulk_file.close()
############################################################

############################################################
def check_difference_urls(file_path, url_array):
    new_url_lists = []
    with open(file_path, 'r+') as file:
        old_data_lines = file.readlines()
        for new_url in url_array:
            if (new_url+"\n") not in old_data_lines:
                file.writelines(new_url+"\n")
                new_url_lists.append(new_url)
    return new_url_lists
############################################################

############################################################
def set_telegram_url_config(config):
    TOKEN = config["token"]
    chat_id = config["channel_id"]
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}"
    return url
############################################################


############################################################
def send_message_to_group(domains,wildcard_domains,url):
    
    if (len(domains)>0):
        domains_list ="Doamins URLs : \n"
        for domain in domains:
            domains_list += domain+"\n"

        if len(domains_list) > 4095:
            print("Too Long Message")
            for x in range(0, len(domains_list), 4095):
                urls = url + f"&text={domains_list[x:x+4095]}"
                res = requests.get(urls).json() # this sends the message
        else:
            urls = url + f"&text={domains_list}"
            res = requests.get(urls).json() # this sends the message

    if (len(wildcard_domains)>0):

        wildcard_list ="WildCards URLs : \n"
        for wildcard in wildcard_domains:
            wildcard_list += wildcard+"\n"

        if len(wildcard_list) > 4095:
            print("Too Long Message")
            for x in range(0, len(wildcard_list), 4095):
                urls = url + f"&text={wildcard_list[x:x+4095]}"
                res = requests.get(urls).json() # this sends the message
                
        else:
            urls = url + f"&text={wildcard_list}"
            requests.get(urls).json() # this sends the message

    print("Successfully")
############################################################

############################################################
if __name__ == "__main__":
    config_data = read_config_file()
    url = set_telegram_url_config(config_data)
    counter = 0
    while True:
        domains,wildCards = get_new_domains_update()
        check_file_exist("./db/domains.txt",domains)
        check_file_exist("./db/wildcards.txt",wildCards)

        new_domains = check_difference_urls("./db/domains.txt",domains)
        new_wildCards = check_difference_urls("./db/wildcards.txt",wildCards)

        send_message_to_group(new_domains,new_wildCards,url)

        counter+=1
        if counter > 11 :
            urls = url+"&text= Bot is Live :)"
            requests.get(urls).json() # this sends the message
            counter = 0
        time.sleep(300)
############################################################
