from datetime import datetime
import requests
import threading
from secrets import randbelow, choice
import random
import time
import json
import sys
from os import system
import colorama
from colorama import Fore, Style
from threading import Lock

print_lock = Lock()
colorama.init(autoreset=True)

def error(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, Fore.RED + task_id + Style.RESET_ALL, Fore.RED + text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()


def success(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, Fore.GREEN + task_id + Style.RESET_ALL, Fore.GREEN + text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()

def status(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, task_id, text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()

#generate random password
def gen_ran_passw():
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    chars = ["!","?","=","&","$","#"]
    random_password = ""
    oldvalue = ""
    choicelist = [0,1,2]
    for x in range(14):
        if oldvalue:
            choicelist.remove(oldvalue)
            value = choice(choicelist)
            choicelist.append(oldvalue)
        else:
            value = randbelow(3)
        if value == 0:
            if randbelow(2) == 0:
                random_password += letters[randbelow(len(letters))].upper()
            else:
                random_password += letters[randbelow(len(letters))]
        elif value == 1:
            random_password += chars[randbelow(len(chars))]
        elif value == 2:
            random_password += str(randbelow(10))
        oldvalue = value
    
    random_password += letters[randbelow(len(letters))].upper() + letters[randbelow(len(letters))]
    random_password += chars[randbelow(len(chars))] + str(randbelow(10))

    return random_password

#opening proxyfile and deleting used proxy
def get_session_proxy():
    with open('files/proxies.txt', 'r') as proxy_file:
        read_proxies = proxy_file.read()
    if len(read_proxies) < 2:
        raise ValueError("no proxies in proxylist")
    proxies = read_proxies.splitlines()
    if len(proxies[0]) > 1:
        proxy = proxies[0]
        del proxies[0]
        with open('files/proxies.txt', 'w') as new_proxy_file:
            new_proxy_file.write('\n'.join(proxies))
    
    proxy_info = proxy.split(':')
    final_proxies = {
        "http": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}",
        "https": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}"
    }
    return final_proxies

#generates random client id
def gen_client_id():
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    ran4letters = ""
    for _ in range(4):
        if random.randint(0,1) == 0:
            ran4letters += letters[random.randrange(0,len(letters))]
        else:
            ran4letters += letters[random.randrange(0,len(letters))].upper()
    ran15chars = ""
    for _ in range(15):
        if random.randint(0,1) == 0:
            if random.randint(0,1) == 0:
                ran15chars += letters[random.randrange(0,len(letters))]
            else:
                ran15chars += letters[random.randrange(0,len(letters))].upper()
        else:
            ran15chars += str(random.randint(0,9))

    client_id = f'Yf{ran4letters}ALAAG{letters[random.randrange(0,len(letters))].upper() + ran15chars}'
    return client_id

def genLoginHeaders(csrf, claim):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'q=0.9,en-US;q=0.8,en;q=0.7',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'x-asbd-id': '198387',
        'x-csrftoken': csrf,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': claim,
        'x-instagram-ajax': '6ab3c34e0025',
        'x-requested-with': 'XMLHttpRequest'
    }
    return headers

def get_random_name():
    names = ["lenniii", "lennartt", "floriian", "maximiliann"] # you need to add a api or smth I just tested with these
    return random.choice(names)+str(random.randint(99, 12345))

def instagen(task_id, smsapi=None, country_code=None, webhook=None):
    if not smsapi or not country_code or smsapi == "YOUR_SMS_API_KEY":
        error('Please check your config file', task_id)
        return
    if country_code not in country_to_phone:
        error('Phone countrycode not supported', task_id)
        return

    #creating session + appending proxies to session
    s = requests.Session()
    try:
        s.proxies = get_session_proxy()
    except ValueError as err:
        error(err, task_id)
        return
        

    #getting device_id and csrf token
    while True:
        try:
            

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
            }
            res = s.get('https://www.instagram.com/accounts/emailsignup/', headers=headers)
            device_id = res.text.split('"device_id":"')[1].split('"')[0]
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.instagram.com/accounts/emailsignup/',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
                'x-asbd-id': '198387',
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
                'x-web-device-id': device_id
            }
            res = s.get('https://www.instagram.com/data/shared_data/', headers=headers)
            csrf = res.text.split('csrf_token":"')[1].split('"')[0]
            break
        except:
            error('Couldnt get device_id, trying again...', task_id)
            s = requests.Session()
            try:
                s.proxies = get_session_proxy()
            except ValueError as err:
                error(err, task_id)
                return
            time.sleep(2)

    time.sleep(0.2)

    password = gen_ran_passw() 
    client_id = gen_client_id()
    name = get_random_name()
    month = str(random.randint(1,12))
    day = str(random.randint(10,25))
    year = str(random.randint(1960,2000))
    username = name
    
    #creation flow:
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/emailsignup/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'x-asbd-id': '198387',
        'x-csrftoken': csrf,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': 'c35f58698901',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    #getting phonenumber and sms code

    for x in range(3):
        #res = s.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country={country_to_phone[country_code]}')
        #try:
        #    phonenum = "+"+res.text.split(':')[2]
        #    phone_id = res.text.split(':')[1]
        #except:
        #    error('Couldn\'t get phone number', task_id)
        
        #    return

        phonenum = input("PHONENUM: ")

        #making first creation attempt
        while True:
            body = {
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'phone_number': phonenum,
                'client_id': client_id,
                'username': username,
                'first_name': name,
                'seamless_login_enabled': '1',
                'opt_into_one_tap': 'false'
            }
            res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
           #checking for error
            try:
                if not res.json()["status"]:
                    error('Account creation failed', task_id)
                    return
            except:
                error('Account creation failed', task_id)
                return
            #checking if username is not available
            if "username" in res.json()["errors"]:
                status('Username already taken... getting new one', task_id)
                username = res.json()["username_suggestions"][0]
            break
        time.sleep(0.4)

        #sending sms to phone number
        body = {          
            'client_id': client_id,
            'phone_number': phonenum,
            "phone_id": "",
            "big_blue_token": ""
        } 
        res = s.post('https://www.instagram.com/accounts/send_signup_sms_code_ajax/', headers=headers, data=body)
        
        status('Waiting for sms code', task_id)
        #receiving sms code
        #for _ in range(10):
        #    res = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=getStatus&id={phone_id}')
        #    try:
        #        sms_code = res.text.split(':')[1]
        #        status('Received sms code', task_id)
        #        break
        #    except:
        #        time.sleep(5)
        #    sms_code = False
        #    time.sleep(3)
        #if sms_code:
        #    #accept sms code on sms-activate
        #    res = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=6&id={phone_id}')
        
        sms_code = input("SMS CODE: ")
        #validating sms code
        body = {
            'client_id': client_id,
            'phone_number': phonenum,
            'sms_code': sms_code
        }
        res = s.post('https://www.instagram.com/accounts/validate_signup_sms_code_ajax/', headers=headers, data=body)
        print(res.status_code)
        status('SMS code is valid', task_id)
        break
        
        #else:
        #    #cancel number
        #    error('Couldnt get sms code... getting new phone number', task_id)
        #    requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=8&id={phone_id}')
        #    time.sleep(1)
    
    status('Sending information...', task_id)
    body = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'phone_number': phonenum,
        'client_id': client_id,
        'username': username,
        'first_name': name,
        'sms_code': sms_code,
        'seamless_login_enabled': '1'
    }
    res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
    time.sleep(0.5)

    #final request
    body["month"] = month
    body["day"] = day
    body["year"] = year
    body["tos_version"] = 'eu'
    res = s.post('https://www.instagram.com/accounts/web_create_ajax/', headers=headers, data=body)
    if res.status_code == 200:
        success('Successfully created account', task_id)
    else:
        error('Account creation failed', task_id)
        return

    #sleeping then checking if acc got clipped
    status('Checking if the account got clipped', task_id)
    time.sleep(15)                      #you can play with this delay and make it lower
    
    for retries in range(3):
        #getting first csrf token
        res = s.get('https://www.instagram.com/accounts/login/')
        csrf = res.text.split('csrf_token":"')[1].split('"')[0]
        insta_claim = "0"

        #payload for login
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        #trying to login
        headers = genLoginHeaders(csrf, insta_claim)
        res = s.post('https://www.instagram.com/accounts/login/ajax/', headers=headers, data=payload)
        try:
            if res.json()["authenticated"]:                 #successfull logged in:
                status('Logged in', task_id)
                insta_claim = res.headers["x-ig-set-www-claim"]
                csrf = s.cookies.get_dict()["csrftoken"]
                headers = genLoginHeaders(csrf, insta_claim)
                time.sleep(1)
                res = s.post(f'https://www.instagram.com/web/friendships/6860189/follow/', headers=headers, data={})
                try:
                    #account got clipped
                    if res.json()["message"]:
                        error('Account got clipped', task_id)
                        #clipurl = res.json()["checkpoint_url"]
                        with open('files/clipped_accounts.txt', 'a') as acc_file:
                            acc_file.write(f'{username}:{password}\n')
                except:
                    #account is not clipped!
                    success('Account is valid', task_id)
                    with open('files/working_accounts.txt', 'a') as acc_file:
                        acc_file.write(f'{username}:{password}\n')
                    #sending message to discord webhook if specified
                    if webhook:
                        webhook_body = {
                            "content": None,
                            "embeds": [
                                {
                                    "title": "Successful Instragram Account Created",
                                    "color": 720640,
                                    "fields": [
                                        {
                                            "name": "username",
                                            "value": f"||{username}||",
                                            "inline": True
                                        },
                                        {
                                            "name": "Password",
                                            "value": f"||{password}||",
                                            "inline": True
                                        }
                                    ],
                                    "thumbnail": {
                                        "url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                                    }
                                }
                            ],
                            "username": "Instagram Gen",
                            "avatar_url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                        }
                        res = requests.post(webhook, data=json.dumps(webhook_body), headers={"Content-Type":"application/json"})
                break
            else:
                #login failed
                if retries < 2:
                    error('Login failed', task_id)
                    status('Switching proxies and retrying in 15 seconds again', task_id)
                    s = requests.Session()
                    try:
                        s.proxies = get_session_proxy()
                    except ValueError as err:
                        error(err, i)
                        return
                    time.sleep(15)                  #change the retry delay to what you like
                else:
                    error('Login failed -> stopping task', task_id)
                    return
                    
        
        except Exception as e:
            #login failed
            if retries < 2:
                error('Login failed', task_id)
                status('Switching proxies and retrying in 15 seconds again', task_id)
                s = requests.Session()
                try:
                    s.proxies = get_session_proxy()
                except ValueError as err:
                    error(err, task_id)
                    return
                time.sleep(15)                      #change the retry delay to what you like
            else:
                error('Login failed -> stopping task', task_id)
                return

country_to_phone = {
    "DE": "43",
    "IT": "86",
    "ES": "56",
    "FR": "78"
}

with open('files/proxies.txt', 'r') as proxy_file:
    read_proxies = proxy_file.read()
    if len(read_proxies) < 2:
        print('proxy file empty -> continue without proxies')

with open("files/config.json", "r") as config_file:
    read_config = json.load(config_file)
sms_api_key = read_config["sms_api_key"]
webhook_url = read_config["webhook_url"]

system('title Instagram Gen - made by @devlenni - devlenni#5659')

HEADER = """


                        ____           __                                      ______         
                       /  _/___  _____/ /_____ _____ __________ _____ ___     / ____/__  ____ 
                       / // __ \/ ___/ __/ __ `/ __ `/ ___/ __ `/ __ `__ \   / / __/ _ \/ __ \ 
                     _/ // / / (__  ) /_/ /_/ / /_/ / /  / /_/ / / / / / /  / /_/ /  __/ / / /
                    /___/_/ /_/____/\__/\__,_/\__, /_/   \__,_/_/ /_/ /_/   \____/\___/_/ /_/ 
                                             /____/                                           






"""
print(Fore.MAGENTA, HEADER, Style.RESET_ALL)

print('how many accounts?')
ts = int(input('>>> '))
threadlist = []
for i in range(ts):
    i = str(i).replace(" ", "")
    t = threading.Thread(target=lambda h=i:instagen(str(h), smsapi=sms_api_key, country_code="DE", webhook=webhook_url))
    threadlist.append(t)
    status('Starting generation...', i)
    t.start()
    time.sleep(0.3)

#wait till all tasks finished
for thread in threadlist:
    thread.join()

input("press enter to exit...")
